"""
MVXWorld Room — Graybox Blockout Script
Run in Blender 4.0+ to generate the basic room structure.

Usage:
1. Open Blender
2. Switch to Scripting workspace
3. Open this file or paste contents
4. Click "Run Script"

Generates:
- Room shell (walls, floor, ceiling)
- Window openings (3)
- Zone boundaries
- Human figure (basic)
- Camera positions
"""

import bpy
import bmesh
from mathutils import Vector
import math

# ============================================================
# CONFIGURATION
# ============================================================

ROOM = {
    "width": 8.0,
    "depth": 10.0,
    "height": 3.5,
    "wall_thickness": 0.15,
    "floor_thickness": 0.10,
    "ceiling_thickness": 0.20,
}

WINDOWS = [
    {"name": "North", "pos": (0, -ROOM["depth"] / 2, 1.2), "size": (1.5, 2.5)},
    {"name": "East", "pos": (ROOM["width"] / 2, -2.0, 1.2), "size": (1.5, 2.5)},
    {"name": "South", "pos": (0, ROOM["depth"] / 2 - 1.0, 1.2), "size": (1.5, 2.5)},
]

ZONES = {
    "Central_Core": {
        "pos": (0, 0, 0),
        "size": (3.0, 4.0),
        "color": (0.8, 0.2, 0.2, 0.3),
    },
    "Memory_Wall": {
        "pos": (0, -ROOM["depth"] / 2 + 0.25, 0),
        "size": (8.0, 0.5),
        "color": (0.2, 0.8, 0.2, 0.3),
    },
    "Transmission_Zone": {
        "pos": (3.5, -3.0, 0),
        "size": (2.5, 2.5),
        "color": (0.2, 0.2, 0.8, 0.3),
    },
    "Archive_Shelves": {
        "pos": (-3.5, -2.0, 0),
        "size": (3.0, 0.6),
        "color": (0.8, 0.8, 0.2, 0.3),
    },
    "Discovery_Zone": {
        "pos": (0, 3.0, 0),
        "size": (4.0, 3.0),
        "color": (0.8, 0.2, 0.8, 0.3),
    },
}

CAMERA_SHOTS = [
    {"name": "Arrival", "pos": (0, 8.0, 1.65), "target": (0, 0, 1.2), "lens": 24},
    {"name": "Desk", "pos": (1.5, 1.5, 1.15), "target": (0, 0, 0.75), "lens": 50},
    {"name": "Wall", "pos": (0, -3.0, 1.65), "target": (0, -5.0, 1.8), "lens": 35},
    {
        "name": "Signal",
        "pos": (2.5, -1.5, 1.65),
        "target": (3.5, -3.0, 1.8),
        "lens": 50,
    },
    {
        "name": "Shelves",
        "pos": (-2.5, -1.0, 1.2),
        "target": (-3.5, -2.0, 1.5),
        "lens": 85,
    },
    {"name": "Experiment", "pos": (0, 4.0, 1.65), "target": (0, 3.0, 1.5), "lens": 35},
    {
        "name": "Window",
        "pos": (3.0, -4.0, 1.65),
        "target": (3.5, -5.0, 2.0),
        "lens": 24,
    },
    {"name": "Overview", "pos": (2.0, 2.0, 2.5), "target": (0, -2.0, 1.0), "lens": 18},
    {"name": "Detail", "pos": (0.3, 0.3, 0.9), "target": (0, 0, 0.75), "lens": 85},
    {"name": "Exit", "pos": (0, -6.0, 1.65), "target": (0, 8.0, 1.65), "lens": 35},
]

HUMAN_HEIGHT = 1.75  # meters

# ============================================================
# UTILITIES
# ============================================================


def clean_scene():
    """Remove all objects from scene."""
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    # Remove all collections except Scene Collection
    for col in bpy.data.collections:
        bpy.data.collections.remove(col)


def create_collection(name):
    """Create a new collection."""
    col = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(col)
    return col


def link_to_collection(obj, collection):
    """Link object to specific collection."""
    collection.objects.link(obj)
    # Remove from scene collection if present
    if obj.name in bpy.context.scene.collection.objects:
        bpy.context.scene.collection.objects.unlink(obj)


def set_origin_to_geometry(obj):
    """Set object origin to geometry center."""
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="MEDIAN")


# ============================================================
# ROOM CONSTRUCTION
# ============================================================


def create_floor():
    """Create the floor."""
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
    floor = bpy.context.active_object
    floor.name = "Floor"
    floor.scale = (ROOM["width"], ROOM["depth"], 1)
    bpy.ops.object.transform_apply(scale=True)

    # Add thickness
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.extrude_region_move(
        TRANSFORM_OT_translate={"value": (0, 0, -ROOM["floor_thickness"])}
    )
    bpy.ops.object.mode_set(mode="OBJECT")

    return floor


def create_ceiling():
    """Create the ceiling."""
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, ROOM["height"]))
    ceiling = bpy.context.active_object
    ceiling.name = "Ceiling"
    ceiling.scale = (ROOM["width"], ROOM["depth"], 1)
    bpy.ops.object.transform_apply(scale=True)

    # Add thickness
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.extrude_region_move(
        TRANSFORM_OT_translate={"value": (0, 0, ROOM["ceiling_thickness"])}
    )
    bpy.ops.object.mode_set(mode="OBJECT")

    return ceiling


def create_wall(name, start, end, height, thickness):
    """Create a wall segment."""
    # Calculate wall center and dimensions
    center = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2, height / 2)
    length = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
    rotation = math.atan2(end[1] - start[1], end[0] - start[0])

    bpy.ops.mesh.primitive_cube_add(size=1, location=center)
    wall = bpy.context.active_object
    wall.name = name
    wall.scale = (length, thickness, height)
    wall.rotation_euler[2] = rotation
    bpy.ops.object.transform_apply(scale=True, rotation=True)

    return wall


def create_walls():
    """Create all four walls with window openings."""
    walls = []
    h = ROOM["height"]
    t = ROOM["wall_thickness"]
    w = ROOM["width"]
    d = ROOM["depth"]

    # North wall (y = -depth/2)
    # Split into sections around window
    win = WINDOWS[0]
    win_x = win["pos"][0]
    win_w = win["size"][0]
    win_h = win["size"][1]
    win_z = win["pos"][2]

    # Left section
    if win_x - win_w / 2 > -w / 2:
        walls.append(
            create_wall(
                "Wall_North_Left", (-w / 2, -d / 2), (win_x - win_w / 2, -d / 2), h, t
            )
        )

    # Right section
    if win_x + win_w / 2 < w / 2:
        walls.append(
            create_wall(
                "Wall_North_Right", (win_x + win_w / 2, -d / 2), (w / 2, -d / 2), h, t
            )
        )

    # Top section (above window)
    walls.append(
        create_wall(
            "Wall_North_Top",
            (win_x - win_w / 2, -d / 2),
            (win_x + win_w / 2, -d / 2),
            h - (win_z + win_h / 2),
            t,
        )
    )

    # Bottom section (below window)
    walls.append(
        create_wall(
            "Wall_North_Bottom",
            (win_x - win_w / 2, -d / 2),
            (win_x + win_w / 2, -d / 2),
            win_z - win_h / 2,
            t,
        )
    )

    # South wall (y = +depth/2)
    win = WINDOWS[2]
    win_x = win["pos"][0]
    win_w = win["size"][0]
    win_h = win["size"][1]
    win_z = win["pos"][2]

    if win_x - win_w / 2 > -w / 2:
        walls.append(
            create_wall(
                "Wall_South_Left", (-w / 2, d / 2), (win_x - win_w / 2, d / 2), h, t
            )
        )

    if win_x + win_w / 2 < w / 2:
        walls.append(
            create_wall(
                "Wall_South_Right", (win_x + win_w / 2, d / 2), (w / 2, d / 2), h, t
            )
        )

    walls.append(
        create_wall(
            "Wall_South_Top",
            (win_x - win_w / 2, d / 2),
            (win_x + win_w / 2, d / 2),
            h - (win_z + win_h / 2),
            t,
        )
    )

    walls.append(
        create_wall(
            "Wall_South_Bottom",
            (win_x - win_w / 2, d / 2),
            (win_x + win_w / 2, d / 2),
            win_z - win_h / 2,
            t,
        )
    )

    # East wall (x = +width/2)
    win = WINDOWS[1]
    win_y = win["pos"][1]
    win_w = win["size"][0]
    win_h = win["size"][1]
    win_z = win["pos"][2]

    walls.append(create_wall("Wall_East", (w / 2, -d / 2), (w / 2, d / 2), h, t))

    # West wall (x = -width/2)
    walls.append(create_wall("Wall_West", (-w / 2, -d / 2), (-w / 2, d / 2), h, t))

    return walls


def create_window_frame(name, position, size):
    """Create a window frame."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=position)
    frame = bpy.context.active_object
    frame.name = name
    frame.scale = (size[0], 0.05, size[1])
    bpy.ops.object.transform_apply(scale=True)

    return frame


def create_windows():
    """Create all window frames."""
    frames = []
    for i, win in enumerate(WINDOWS):
        frame = create_window_frame(f"Window_{win['Name']}", win["pos"], win["size"])
        frames.append(frame)
    return frames


# ============================================================
# ZONE BOUNDARIES
# ============================================================


def create_zone_marker(name, position, size, color):
    """Create a zone boundary marker (flat plane)."""
    bpy.ops.mesh.primitive_plane_add(
        size=1,
        location=(position[0], position[1], 0.001),  # Slightly above floor
    )
    zone = bpy.context.active_object
    zone.name = f"Zone_{name}"
    zone.scale = (size[0], size[1], 1)
    bpy.ops.object.transform_apply(scale=True)

    # Create material
    mat = bpy.data.materials.new(name=f"MAT_Zone_{name}")
    mat.use_nodes = True
    mat.blend_method = "BLEND"  # For Eevee transparency

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    # Create nodes
    output = nodes.new("ShaderNodeOutputMaterial")
    output.location = (400, 0)

    emission = nodes.new("ShaderNodeEmission")
    emission.location = (200, 0)
    emission.inputs["Color"].default_value = color
    emission.inputs["Strength"].default_value = 0.5

    transparent = nodes.new("ShaderNodeBsdfTransparent")
    transparent.location = (0, 0)

    mix = nodes.new("ShaderNodeMixShader")
    mix.location = (200, -100)
    mix.inputs["Fac"].default_value = 0.7  # Mostly transparent

    # Connect nodes
    links.new(transparent.outputs["BSDF"], mix.inputs[1])
    links.new(emission.outputs["Emission"], mix.inputs[2])
    links.new(mix.outputs["Shader"], output.inputs["Surface"])

    zone.data.materials.append(mat)

    return zone


def create_zones():
    """Create all zone markers."""
    zones = []
    for name, data in ZONES.items():
        zone = create_zone_marker(name, data["pos"], data["size"], data["color"])
        zones.append(zone)
    return zones


# ============================================================
# HUMAN FIGURE
# ============================================================


def create_human_figure():
    """Create a simple human figure for scale reference."""
    # Head
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.1, location=(0, 0, HUMAN_HEIGHT - 0.1)
    )
    head = bpy.context.active_object
    head.name = "Human_Head"

    # Body
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.15, depth=0.6, location=(0, 0, HUMAN_HEIGHT - 0.5)
    )
    body = bpy.context.active_object
    body.name = "Human_Body"

    # Legs
    bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.8, location=(0.05, 0, 0.4))
    leg_r = bpy.context.active_object
    leg_r.name = "Human_Leg_R"

    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.06, depth=0.8, location=(-0.05, 0, 0.4)
    )
    leg_l = bpy.context.active_object
    leg_l.name = "Human_Leg_L"

    # Arms
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.04, depth=0.6, location=(0.2, 0, HUMAN_HEIGHT - 0.6)
    )
    arm_r = bpy.context.active_object
    arm_r.name = "Human_Arm_R"
    arm_r.rotation_euler[2] = math.radians(15)

    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.04, depth=0.6, location=(-0.2, 0, HUMAN_HEIGHT - 0.6)
    )
    arm_l = bpy.context.active_object
    arm_l.name = "Human_Arm_L"
    arm_l.rotation_euler[2] = math.radians(-15)

    # Create wire material
    mat = bpy.data.materials.new(name="MAT_Human_Reference")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    principled = nodes.get("Principled BSDF")
    principled.inputs["Base Color"].default_value = (0.5, 0.5, 0.5, 1)
    principled.inputs["Alpha"].default_value = 0.3

    for obj in [head, body, leg_r, leg_l, arm_r, arm_l]:
        obj.data.materials.append(mat)
        obj.display_type = "WIRE"

    # Parent all to empty
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0, 0, 0))
    parent = bpy.context.active_object
    parent.name = "Human_Figure"

    for obj in [head, body, leg_r, leg_l, arm_r, arm_l]:
        obj.parent = parent

    return parent


# ============================================================
# CAMERAS
# ============================================================


def create_cameras():
    """Create all cinematic cameras."""
    cameras = []

    for shot in CAMERA_SHOTS:
        bpy.ops.object.camera_add(location=shot["pos"])
        cam = bpy.context.active_object
        cam.name = f"CAM_{shot['name']}"
        cam.data.lens = shot["lens"]

        # Point at target
        direction = Vector(shot["target"]) - cam.location
        rot_quat = direction.to_track_quat("-Z", "Y")
        cam.rotation_euler = rot_quat.to_euler()

        cameras.append(cam)

    return cameras


# ============================================================
# MATERIALS
# ============================================================


def create_basic_materials():
    """Create basic placeholder materials."""
    materials = {
        "MAT_Aged_Walnut": {
            "color": (0.24, 0.17, 0.12, 1),
            "roughness": 0.75,
            "metallic": 0.0,
        },
        "MAT_Brushed_Metal": {
            "color": (0.54, 0.54, 0.54, 1),
            "roughness": 0.50,
            "metallic": 0.85,
        },
        "MAT_Glass": {"color": (0.8, 0.9, 1.0, 1), "roughness": 0.10, "metallic": 0.0},
        "MAT_Paper": {
            "color": (0.96, 0.95, 0.93, 1),
            "roughness": 0.90,
            "metallic": 0.0,
        },
        "MAT_Leather": {
            "color": (0.16, 0.12, 0.08, 1),
            "roughness": 0.60,
            "metallic": 0.0,
        },
        "MAT_Stone": {
            "color": (0.23, 0.23, 0.22, 1),
            "roughness": 0.85,
            "metallic": 0.0,
        },
        "MAT_Brass": {
            "color": (0.71, 0.65, 0.26, 1),
            "roughness": 0.40,
            "metallic": 0.90,
        },
        "MAT_Emissive_Acid": {
            "color": (0.78, 1.0, 0.0, 1),
            "roughness": 0.20,
            "metallic": 0.70,
        },
        "MAT_Wall": {
            "color": (0.10, 0.10, 0.09, 1),
            "roughness": 0.80,
            "metallic": 0.0,
        },
        "MAT_Floor": {
            "color": (0.15, 0.12, 0.10, 1),
            "roughness": 0.70,
            "metallic": 0.0,
        },
    }

    created = {}

    for name, props in materials.items():
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True

        nodes = mat.node_tree.nodes
        principled = nodes.get("Principled BSDF")

        principled.inputs["Base Color"].default_value = props["color"]
        principled.inputs["Roughness"].default_value = props["roughness"]
        principled.inputs["Metallic"].default_value = props["metallic"]

        if name == "MAT_Emissive_Acid":
            principled.inputs["Emission Color"].default_value = props["color"]
            principled.inputs["Emission Strength"].default_value = 5.0

        created[name] = mat

    return created


# ============================================================
# LIGHTING
# ============================================================


def create_lighting():
    """Create basic lighting setup."""
    lights = []

    # Sun (key light)
    bpy.ops.object.light_add(type="SUN", location=(0, 0, ROOM["height"] + 1))
    sun = bpy.context.active_object
    sun.name = "LIGHT_Sun"
    sun.data.energy = 5.0
    sun.data.color = (1.0, 0.95, 0.9)  # 5500K warm
    sun.rotation_euler = (math.radians(35), 0, math.radians(220))
    lights.append(sun)

    # Desk lamp (warm spot)
    bpy.ops.object.light_add(type="SPOT", location=(0, 0, 1.5))
    desk_lamp = bpy.context.active_object
    desk_lamp.name = "LIGHT_DeskLamp"
    desk_lamp.data.energy = 800  # lumens
    desk_lamp.data.color = (1.0, 0.8, 0.6)  # 2700K warm
    desk_lamp.data.spot_size = math.radians(60)
    lights.append(desk_lamp)

    # Window fill (area)
    for i, win in enumerate(WINDOWS):
        bpy.ops.object.light_add(type="AREA", location=win["pos"])
        window_light = bpy.context.active_object
        window_light.name = f"LIGHT_Window_{win['Name']}"
        window_light.data.energy = 15000
        window_light.data.color = (1.0, 0.98, 0.95)  # 5500K
        window_light.data.size = win["size"][0]
        lights.append(window_light)

    return lights


# ============================================================
# WORLD SETTINGS
# ============================================================


def setup_world():
    """Setup world environment."""
    world = bpy.data.worlds.new("MVXWorld_Environment")
    bpy.context.scene.world = world

    world.use_nodes = True
    nodes = world.node_tree.nodes
    links = world.node_tree.links

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    # Create nodes
    output = nodes.new("ShaderNodeOutputWorld")
    output.location = (400, 0)

    background = nodes.new("ShaderNodeBackground")
    background.location = (200, 0)
    background.inputs["Color"].default_value = (0.02, 0.02, 0.02, 1)  # Very dark
    background.inputs["Strength"].default_value = 0.5

    links.new(background.outputs["Background"], output.inputs["Surface"])

    return world


# ============================================================
# RENDER SETTINGS
# ============================================================


def setup_render():
    """Configure render settings."""
    scene = bpy.context.scene

    # Resolution
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100

    # Engine
    scene.render.engine = "BLENDER_EEVEE"  # Start with Eevee for speed

    # Eevee settings (handle Blender 4.0+ API changes)
    eevee = scene.eevee
    try:
        if hasattr(eevee, "use_ssr"):
            eevee.use_ssr = True
        if hasattr(eevee, "use_ssr_refraction"):
            eevee.use_ssr_refraction = True
        if hasattr(eevee, "use_gtao"):
            eevee.use_gtao = True
        if hasattr(eevee, "use_ambient_occlusion"):
            eevee.use_ambient_occlusion = True
        if hasattr(eevee, "use_bloom"):
            eevee.use_bloom = True
            eevee.bloom_intensity = 0.1
    except Exception as e:
        print(f"[RENDER] Some settings skipped: {e}")

    # Output
    scene.render.filepath = "//renders/"
    scene.render.image_settings.file_format = "PNG"

    return scene


# ============================================================
# MAIN EXECUTION
# ============================================================


def main():
    """Main execution function."""
    print("=" * 50)
    print("MVXWorld Room — Graybox Blockout")
    print("=" * 50)

    # Clean scene
    print("\n[1/8] Cleaning scene...")
    clean_scene()

    # Create collections
    print("[2/8] Creating collections...")
    col_room = create_collection("Room")
    col_zones = create_collection("Zones")
    col_ref = create_collection("Reference")
    col_lights = create_collection("Lights")
    col_cameras = create_collection("Cameras")

    # Create room shell
    print("[3/8] Creating room shell...")
    floor = create_floor()
    link_to_collection(floor, col_room)

    ceiling = create_ceiling()
    link_to_collection(ceiling, col_room)

    walls = create_walls()
    for wall in walls:
        link_to_collection(wall, col_room)

    # Create windows
    print("[4/8] Creating windows...")
    windows = create_windows()
    for win in windows:
        link_to_collection(win, col_room)

    # Create zones
    print("[5/8] Creating zone markers...")
    zones = create_zones()
    for zone in zones:
        link_to_collection(zone, col_zones)

    # Create human figure
    print("[6/8] Creating human figure...")
    human = create_human_figure()
    link_to_collection(human, col_ref)

    # Create cameras
    print("[7/8] Creating cameras...")
    cameras = create_cameras()
    for cam in cameras:
        link_to_collection(cam, col_cameras)

    # Create materials
    print("[8/8] Creating materials...")
    materials = create_basic_materials()

    # Setup lighting
    print("\n[LIGHTS] Creating lighting setup...")
    lights = create_lighting()
    for light in lights:
        link_to_collection(light, col_lights)

    # Setup world
    print("[WORLD] Setting up environment...")
    setup_world()

    # Setup render
    print("[RENDER] Configuring render settings...")
    setup_render()

    # Apply materials to room
    print("\n[MATERIALS] Applying materials...")
    floor.data.materials.append(materials["MAT_Floor"])
    ceiling.data.materials.append(materials["MAT_Wall"])
    for wall in walls:
        wall.data.materials.append(materials["MAT_Wall"])

    # Set default camera
    if cameras:
        bpy.context.scene.camera = cameras[0]  # Arrival shot

    # Deselect all
    bpy.ops.object.select_all(action="DESELECT")

    print("\n" + "=" * 50)
    print("GRAYBOX COMPLETE")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Save as 'MVXWorld_Room.blend'")
    print("2. Check scale with human figure")
    print("3. Test camera shots")
    print("4. Begin hero asset modeling")
    print("\nZone colors (translucent):")
    for name in ZONES:
        print(f"  - {name}")


# Run if executed as script
if __name__ == "__main__":
    main()
