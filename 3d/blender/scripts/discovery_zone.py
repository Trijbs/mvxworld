"""
MVXWorld — Discovery / Experiment Zone
Run in Blender 4.0+ after graybox is loaded.

Usage:
1. Open MVXWorld_Room.blend
2. Switch to Scripting workspace
3. Open this file or paste contents
4. Click "Run Script"

Generates:
- Experiment workbench
- Floating geometric objects (8)
- Half-finished mechanical inventions (3)
- Interactive abstract devices (4)
- Unknown physics mechanisms (2)
- Suspended experimental forms (5)
- Specialized tool rack
"""

import bpy
import math
from mathutils import Vector, noise

# ============================================================
# CONFIGURATION
# ============================================================

ZONE = {
    "center": (0, 3.0, 0),
    "size": (4.0, 3.0),
}

WORKBENCH = {
    "width": 1.5,
    "depth": 0.8,
    "height": 0.75,
    "thickness": 0.04,
}

FLOATING_OBJECTS = {
    "count": 8,
    "min_size": 0.05,
    "max_size": 0.2,
    "float_height_min": 0.8,
    "float_height_max": 2.0,
}

INVENTIONS = {
    "count": 3,
    "max_size": 0.4,
}

DEVICES = {
    "count": 4,
    "base_size": 0.15,
}

MECHANISMS = {
    "count": 2,
    "size": 0.25,
}

SUSPENDED = {
    "count": 5,
    "height_min": 2.0,
    "height_max": 2.8,
}

TOOLS = {
    "count": 10,
    "rack_width": 0.8,
}

# ============================================================
# UTILITIES
# ============================================================


def clean_name(prefix, name):
    """Create clean object name."""
    return f"MESH_{prefix}_{name}"


def create_material(
    name, color, roughness=0.7, metallic=0.0, emission=None, emission_strength=0
):
    """Create or get material."""
    if name in bpy.data.materials:
        return bpy.data.materials[name]

    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True

    nodes = mat.node_tree.nodes
    principled = nodes.get("Principled BSDF")

    principled.inputs["Base Color"].default_value = (*color, 1)
    principled.inputs["Roughness"].default_value = roughness
    principled.inputs["Metallic"].default_value = metallic

    if emission:
        principled.inputs["Emission Color"].default_value = (*emission, 1)
        principled.inputs["Emission Strength"].default_value = emission_strength

    return mat


def add_bevel(obj, width=0.002, segments=2):
    """Add bevel modifier."""
    bevel = obj.modifiers.new(name="Bevel", type="BEVEL")
    bevel.width = width
    bevel.segments = segments
    bevel.limit_method = "ANGLE"
    bevel.angle_limit = math.radians(30)
    return bevel


# ============================================================
# WORKBENCH
# ============================================================


def create_workbench():
    """Create the experiment workbench."""
    x, y, z = ZONE["center"]
    parts = []

    # Table top
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z + WORKBENCH["height"]))
    top = bpy.context.active_object
    top.name = clean_name("Bench", "Top")
    top.scale = (WORKBENCH["width"], WORKBENCH["depth"], WORKBENCH["thickness"])
    bpy.ops.object.transform_apply(scale=True)
    add_bevel(top, width=0.005)
    parts.append(top)

    # Legs
    leg_positions = [
        (-WORKBENCH["width"] / 2 + 0.08, -WORKBENCH["depth"] / 2 + 0.08),
        (-WORKBENCH["width"] / 2 + 0.08, WORKBENCH["depth"] / 2 - 0.08),
        (WORKBENCH["width"] / 2 - 0.08, -WORKBENCH["depth"] / 2 + 0.08),
        (WORKBENCH["width"] / 2 - 0.08, WORKBENCH["depth"] / 2 - 0.08),
    ]

    for i, (lx, ly) in enumerate(leg_positions):
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.025,
            depth=WORKBENCH["height"],
            location=(x + lx, y + ly, z + WORKBENCH["height"] / 2),
        )
        leg = bpy.context.active_object
        leg.name = clean_name("Bench", f"Leg_{i}")
        parts.append(leg)

    # Back board
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(x, y - WORKBENCH["depth"] / 2 + 0.02, z + WORKBENCH["height"] + 0.3),
    )
    backboard = bpy.context.active_object
    backboard.name = clean_name("Bench", "BackBoard")
    backboard.scale = (WORKBENCH["width"], 0.02, 0.6)
    bpy.ops.object.transform_apply(scale=True)
    parts.append(backboard)

    # Active project (half-built thing)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(x + 0.3, y, z + WORKBENCH["height"] + WORKBENCH["thickness"] + 0.05),
    )
    project = bpy.context.active_object
    project.name = clean_name("Bench", "ActiveProject")
    project.scale = (0.3, 0.2, 0.1)
    project.rotation_euler[2] = math.radians(15)
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    add_bevel(project, width=0.003)
    parts.append(project)

    return parts


# ============================================================
# FLOATING GEOMETRIC OBJECTS
# ============================================================


def create_floating_objects():
    """Create floating geometric objects."""
    x, y, z = ZONE["center"]
    parts = []

    geometries = [
        "cube",
        "sphere",
        "cone",
        "torus",
        "ico_sphere",
        "cylinder",
        "monkey",
        "plane",
    ]

    for i in range(FLOATING_OBJECTS["count"]):
        # Random position within zone
        obj_x = x + (noise.random() - 0.5) * 3.0
        obj_y = y + (noise.random() - 0.5) * 2.0
        obj_z = (
            z
            + FLOATING_OBJECTS["float_height_min"]
            + noise.random()
            * (
                FLOATING_OBJECTS["float_height_max"]
                - FLOATING_OBJECTS["float_height_min"]
            )
        )

        size = FLOATING_OBJECTS["min_size"] + noise.random() * (
            FLOATING_OBJECTS["max_size"] - FLOATING_OBJECTS["min_size"]
        )

        geom = geometries[i % len(geometries)]

        if geom == "cube":
            bpy.ops.mesh.primitive_cube_add(size=size, location=(obj_x, obj_y, obj_z))
        elif geom == "sphere":
            bpy.ops.mesh.primitive_uv_sphere_add(
                radius=size / 2, location=(obj_x, obj_y, obj_z)
            )
        elif geom == "cone":
            bpy.ops.mesh.primitive_cone_add(
                radius1=size / 2, radius2=0, depth=size, location=(obj_x, obj_y, obj_z)
            )
        elif geom == "torus":
            bpy.ops.mesh.primitive_torus_add(
                major_radius=size / 2,
                minor_radius=size / 6,
                location=(obj_x, obj_y, obj_z),
            )
        elif geom == "ico_sphere":
            bpy.ops.mesh.primitive_ico_sphere_add(
                radius=size / 2, location=(obj_x, obj_y, obj_z)
            )
        elif geom == "cylinder":
            bpy.ops.mesh.primitive_cylinder_add(
                radius=size / 3, depth=size, location=(obj_x, obj_y, obj_z)
            )
        elif geom == "monkey":
            bpy.ops.mesh.primitive_monkey_add(size=size, location=(obj_x, obj_y, obj_z))
        else:
            bpy.ops.mesh.primitive_plane_add(size=size, location=(obj_x, obj_y, obj_z))

        obj = bpy.context.active_object
        obj.name = clean_name("Floating", f"{geom}_{i:02d}")

        # Random rotation
        obj.rotation_euler[0] = math.radians(noise.random() * 360)
        obj.rotation_euler[1] = math.radians(noise.random() * 360)
        obj.rotation_euler[2] = math.radians(noise.random() * 360)
        bpy.ops.object.transform_apply(rotation=True)

        add_bevel(obj, width=0.002)
        parts.append(obj)

    return parts


# ============================================================
# HALF-FINISHED INVENTIONS
# ============================================================


def create_inventions():
    """Create half-finished mechanical inventions."""
    x, y, z = ZONE["center"]
    parts = []

    invention_configs = [
        # Gear mechanism
        {
            "type": "gears",
            "pos": (x - 0.5, y + 0.5, z + 0.3),
            "components": [
                {"type": "torus", "size": 0.12, "offset": (0, 0, 0)},
                {"type": "torus", "size": 0.08, "offset": (0.15, 0, 0)},
                {"type": "cylinder", "size": 0.02, "offset": (0, 0, 0.05)},
            ],
        },
        # Armature device
        {
            "type": "armature",
            "pos": (x + 0.5, y - 0.3, z + 0.4),
            "components": [
                {"type": "cylinder", "size": 0.03, "offset": (0, 0, 0)},
                {"type": "cylinder", "size": 0.025, "offset": (0, 0, 0.15)},
                {"type": "sphere", "size": 0.04, "offset": (0, 0, 0.3)},
            ],
        },
        # Crystal array
        {
            "type": "crystal",
            "pos": (x, y + 0.8, z + 0.2),
            "components": [
                {"type": "cone", "size": 0.06, "offset": (0, 0, 0)},
                {"type": "cone", "size": 0.04, "offset": (0.08, 0, 0)},
                {"type": "cone", "size": 0.05, "offset": (-0.05, 0.07, 0)},
            ],
        },
    ]

    for inv_idx, config in enumerate(invention_configs):
        inv_x, inv_y, inv_z = config["pos"]

        for comp_idx, comp in enumerate(config["components"]):
            cx, cy, cz = comp["offset"]

            if comp["type"] == "torus":
                bpy.ops.mesh.primitive_torus_add(
                    major_radius=comp["size"],
                    minor_radius=comp["size"] / 4,
                    location=(inv_x + cx, inv_y + cy, inv_z + cz),
                )
            elif comp["type"] == "cylinder":
                bpy.ops.mesh.primitive_cylinder_add(
                    radius=comp["size"],
                    depth=comp["size"] * 3,
                    location=(inv_x + cx, inv_y + cy, inv_z + cz),
                )
            elif comp["type"] == "sphere":
                bpy.ops.mesh.primitive_uv_sphere_add(
                    radius=comp["size"], location=(inv_x + cx, inv_y + cy, inv_z + cz)
                )
            elif comp["type"] == "cone":
                bpy.ops.mesh.primitive_cone_add(
                    radius1=comp["size"],
                    radius2=comp["size"] * 0.2,
                    depth=comp["size"] * 2,
                    location=(inv_x + cx, inv_y + cy, inv_z + cz),
                )

            obj = bpy.context.active_object
            obj.name = clean_name("Invention", f"{config['type']}_{inv_idx}_{comp_idx}")
            obj.rotation_euler[0] = math.radians(noise.random() * 30)
            obj.rotation_euler[1] = math.radians(noise.random() * 30)
            bpy.ops.object.transform_apply(rotation=True)
            add_bevel(obj, width=0.002)
            parts.append(obj)

    return parts


# ============================================================
# INTERACTIVE ABSTRACT DEVICES
# ============================================================


def create_devices():
    """Create interactive abstract devices."""
    x, y, z = ZONE["center"]
    parts = []

    for i in range(DEVICES["count"]):
        dev_x = x + (noise.random() - 0.5) * 2.0
        dev_y = y + (noise.random() - 0.5) * 1.5
        dev_z = z + 0.1

        # Base
        bpy.ops.mesh.primitive_cylinder_add(
            radius=DEVICES["base_size"] / 2, depth=0.03, location=(dev_x, dev_y, dev_z)
        )
        base = bpy.context.active_object
        base.name = clean_name("Device", f"Base_{i}")
        parts.append(base)

        # Central element
        central_types = ["sphere", "cube", "cone"]
        central_type = central_types[i % len(central_types)]

        if central_type == "sphere":
            bpy.ops.mesh.primitive_uv_sphere_add(
                radius=DEVICES["base_size"] / 3, location=(dev_x, dev_y, dev_z + 0.1)
            )
        elif central_type == "cube":
            bpy.ops.mesh.primitive_cube_add(
                size=DEVICES["base_size"] / 2, location=(dev_x, dev_y, dev_z + 0.08)
            )
        else:
            bpy.ops.mesh.primitive_cone_add(
                radius1=DEVICES["base_size"] / 3,
                radius2=0,
                depth=DEVICES["base_size"] / 2,
                location=(dev_x, dev_y, dev_z + 0.1),
            )

        central = bpy.context.active_object
        central.name = clean_name("Device", f"Central_{i}")
        central.rotation_euler[2] = math.radians(i * 45)
        bpy.ops.object.transform_apply(rotation=True)
        parts.append(central)

        # Ring
        bpy.ops.mesh.primitive_torus_add(
            major_radius=DEVICES["base_size"] / 2 + 0.02,
            minor_radius=0.005,
            location=(dev_x, dev_y, dev_z + 0.05),
        )
        ring = bpy.context.active_object
        ring.name = clean_name("Device", f"Ring_{i}")
        parts.append(ring)

    return parts


# ============================================================
# UNKNOWN PHYSICS MECHANISMS
# ============================================================


def create_mechanisms():
    """Create unknown physics-like mechanisms."""
    x, y, z = ZONE["center"]
    parts = []

    for i in range(MECHANISMS["count"]):
        mech_x = x + (i - 0.5) * 1.5
        mech_y = y - 0.5
        mech_z = z + 0.5

        # Frame structure
        bpy.ops.mesh.primitive_cube_add(size=1, location=(mech_x, mech_y, mech_z))
        frame = bpy.context.active_object
        frame.name = clean_name("Mechanism", f"Frame_{i}")
        frame.scale = (MECHANISMS["size"], MECHANISMS["size"] * 0.5, MECHANISMS["size"])
        bpy.ops.object.transform_apply(scale=True)

        # Remove center to make frame
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.mesh.bisect(
            plane_co=(mech_x, mech_y, mech_z), plane_no=(0, 1, 0), clear_inner=True
        )
        bpy.ops.object.mode_set(mode="OBJECT")

        add_bevel(frame, width=0.005)
        parts.append(frame)

        # Orbital spheres
        for j in range(3):
            angle = j * 120
            orb_x = mech_x + math.cos(math.radians(angle)) * MECHANISMS["size"] * 0.4
            orb_y = mech_y
            orb_z = mech_z + math.sin(math.radians(angle)) * MECHANISMS["size"] * 0.4

            bpy.ops.mesh.primitive_uv_sphere_add(
                radius=0.02, location=(orb_x, orb_y, orb_z)
            )
            orb = bpy.context.active_object
            orb.name = clean_name("Mechanism", f"Orb_{i}_{j}")
            parts.append(orb)

    return parts


# ============================================================
# SUSPENDED EXPERIMENTAL FORMS
# ============================================================


def create_suspended_forms():
    """Create suspended experimental forms."""
    x, y, z = ZONE["center"]
    parts = []

    forms = [
        {"type": "crystal", "size": 0.08},
        {"type": "ring", "size": 0.12},
        {"type": "spiral", "size": 0.1},
        {"type": "cluster", "size": 0.06},
        {"type": "lens", "size": 0.15},
    ]

    for i in range(SUSPENDED["count"]):
        form_x = x + (noise.random() - 0.5) * 3.0
        form_y = y + (noise.random() - 0.5) * 2.0
        form_z = (
            z
            + SUSPENDED["height_min"]
            + noise.random() * (SUSPENDED["height_max"] - SUSPENDED["height_min"])
        )

        form = forms[i % len(forms)]

        if form["type"] == "crystal":
            bpy.ops.mesh.primitive_cone_add(
                radius1=form["size"],
                radius2=form["size"] * 0.1,
                depth=form["size"] * 2,
                location=(form_x, form_y, form_z),
            )
        elif form["type"] == "ring":
            bpy.ops.mesh.primitive_torus_add(
                major_radius=form["size"],
                minor_radius=form["size"] / 5,
                location=(form_x, form_y, form_z),
            )
        elif form["type"] == "spiral":
            # Approximate spiral with torus
            bpy.ops.mesh.primitive_torus_add(
                major_radius=form["size"],
                minor_radius=form["size"] / 8,
                location=(form_x, form_y, form_z),
            )
        elif form["type"] == "cluster":
            bpy.ops.mesh.primitive_ico_sphere_add(
                radius=form["size"], location=(form_x, form_y, form_z), subdivisions=1
            )
        else:
            bpy.ops.mesh.primitive_uv_sphere_add(
                radius=form["size"], location=(form_x, form_y, form_z)
            )

        obj = bpy.context.active_object
        obj.name = clean_name("Suspended", f"{form['type']}_{i}")
        obj.rotation_euler[0] = math.radians(noise.random() * 180)
        obj.rotation_euler[1] = math.radians(noise.random() * 180)
        obj.rotation_euler[2] = math.radians(noise.random() * 180)
        bpy.ops.object.transform_apply(rotation=True)
        add_bevel(obj, width=0.002)
        parts.append(obj)

        # Wire/line to ceiling
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.002,
            depth=form_z - (z + 3.0),
            location=(form_x, form_y, (form_z + z + 3.0) / 2),
        )
        wire = bpy.context.active_object
        wire.name = clean_name("Suspended", f"Wire_{i}")
        parts.append(wire)

    return parts


# ============================================================
# TOOL RACK
# ============================================================


def create_tool_rack():
    """Create specialized tool rack."""
    x, y, z = ZONE["center"]
    rack_x = x + 1.5
    rack_y = y + 0.5
    parts = []

    # Rack back
    bpy.ops.mesh.primitive_cube_add(size=1, location=(rack_x, rack_y, z + 1.0))
    back = bpy.context.active_object
    back.name = clean_name("ToolRack", "Back")
    back.scale = (TOOLS["rack_width"], 0.02, 1.5)
    bpy.ops.object.transform_apply(scale=True)
    parts.append(back)

    # Shelves/hooks
    for i in range(3):
        hook_z = z + 0.4 + i * 0.4

        bpy.ops.mesh.primitive_cube_add(
            size=1, location=(rack_x, rack_y + 0.03, hook_z)
        )
        hook = bpy.context.active_object
        hook.name = clean_name("ToolRack", f"Hook_{i}")
        hook.scale = (TOOLS["rack_width"] * 0.8, 0.04, 0.015)
        bpy.ops.object.transform_apply(scale=True)
        parts.append(hook)

    # Tools on rack
    tool_types = ["ruler", "caliper", "marker", "gauge", "probe"]

    for i in range(TOOLS["count"]):
        tool_x = (
            rack_x
            - TOOLS["rack_width"] / 2
            + 0.05
            + i * (TOOLS["rack_width"] / TOOLS["count"])
        )
        tool_z = z + 0.5 + (i % 3) * 0.35

        tool_type = tool_types[i % len(tool_types)]

        if tool_type == "ruler":
            bpy.ops.mesh.primitive_cube_add(
                size=1, location=(tool_x, rack_y + 0.04, tool_z + 0.1)
            )
            obj = bpy.context.active_object
            obj.scale = (0.02, 0.01, 0.2)
        elif tool_type == "caliper":
            bpy.ops.mesh.primitive_cylinder_add(
                radius=0.005,
                depth=0.15,
                location=(tool_x, rack_y + 0.04, tool_z + 0.08),
            )
            obj = bpy.context.active_object
            obj.rotation_euler[0] = math.radians(90)
        elif tool_type == "marker":
            bpy.ops.mesh.primitive_cylinder_add(
                radius=0.006,
                depth=0.12,
                location=(tool_x, rack_y + 0.04, tool_z + 0.06),
            )
            obj = bpy.context.active_object
        elif tool_type == "gauge":
            bpy.ops.mesh.primitive_torus_add(
                major_radius=0.03,
                minor_radius=0.005,
                location=(tool_x, rack_y + 0.04, tool_z + 0.05),
            )
            obj = bpy.context.active_object
        else:
            bpy.ops.mesh.primitive_cone_add(
                radius1=0.008,
                radius2=0.002,
                depth=0.18,
                location=(tool_x, rack_y + 0.04, tool_z + 0.09),
            )
            obj = bpy.context.active_object

        obj.name = clean_name("Tool", f"{tool_type}_{i:02d}")
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        add_bevel(obj, width=0.001)
        parts.append(obj)

    return parts


# ============================================================
# LIGHTING
# ============================================================


def create_lighting():
    """Create discovery zone lighting."""
    x, y, z = ZONE["center"]
    parts = []

    # Ambient warm light
    bpy.ops.object.light_add(type="POINT", location=(x, y, z + 2.5))
    ambient = bpy.context.active_object
    ambient.name = clean_name("Light", "DiscoveryAmbient")
    ambient.data.energy = 800
    ambient.data.color = (0.95, 0.9, 0.85)  # Warm
    ambient.data.shadow_soft_size = 1.0
    parts.append(ambient)

    # Spot on workbench
    bpy.ops.object.light_add(type="SPOT", location=(x, y, z + 2.8))
    spot = bpy.context.active_object
    spot.name = clean_name("Light", "BenchSpot")
    spot.data.energy = 600
    spot.data.color = (1.0, 0.95, 0.9)  # Slightly warm
    spot.data.spot_size = math.radians(60)
    spot.rotation_euler[0] = math.radians(-70)
    parts.append(spot)

    # Accent lights for floating objects
    for i in range(2):
        accent_x = x + (i - 0.5) * 2.0

        bpy.ops.object.light_add(type="POINT", location=(accent_x, y + 0.5, z + 1.5))
        accent = bpy.context.active_object
        accent.name = clean_name("Light", f"FloatingAccent_{i}")
        accent.data.energy = 300
        accent.data.color = (0.9, 0.95, 1.0)  # Slightly cool
        parts.append(accent)

    return parts


# ============================================================
# MATERIALS
# ============================================================


def get_materials():
    """Get or create all materials."""
    materials = {
        "MAT_Wood_Workbench": create_material(
            "MAT_Wood_Workbench", (0.22, 0.15, 0.10), roughness=0.70, metallic=0.0
        ),
        "MAT_Dark_Metal": create_material(
            "MAT_Dark_Metal", (0.12, 0.12, 0.11), roughness=0.40, metallic=0.90
        ),
        "MAT_Brass_Antique": create_material(
            "MAT_Brass_Antique", (0.50, 0.42, 0.18), roughness=0.50, metallic=0.85
        ),
        "MAT_Stone_Dark": create_material(
            "MAT_Stone_Dark", (0.18, 0.17, 0.16), roughness=0.75, metallic=0.0
        ),
        "MAT_Crystal_Glass": create_material(
            "MAT_Crystal_Glass", (0.85, 0.90, 0.95), roughness=0.05, metallic=0.0
        ),
        "MAT_Copper_Patina": create_material(
            "MAT_Copper_Patina", (0.25, 0.45, 0.40), roughness=0.55, metallic=0.80
        ),
        "MAT_Experiment_Glow": create_material(
            "MAT_Experiment_Glow",
            (0.3, 0.8, 0.5),
            roughness=0.20,
            metallic=0.0,
            emission=(0.3, 0.8, 0.5),
            emission_strength=2.0,
        ),
        "MAT_Tool_Steel": create_material(
            "MAT_Tool_Steel", (0.45, 0.45, 0.42), roughness=0.35, metallic=0.90
        ),
    }

    return materials


def apply_materials(objects, materials):
    """Apply materials to objects."""
    material_map = {
        "Bench": "MAT_Wood_Workbench",
        "Leg": "MAT_Dark_Metal",
        "BackBoard": "MAT_Wood_Workbench",
        "ActiveProject": "MAT_Copper_Patina",
        "Floating": ["MAT_Stone_Dark", "MAT_Brass_Antique", "MAT_Crystal_Glass"],
        "Invention": "MAT_Dark_Metal",
        "Device": "MAT_Brass_Antique",
        "Mechanism": "MAT_Crystal_Glass",
        "Orb": "MAT_Experiment_Glow",
        "Suspended": ["MAT_Crystal_Glass", "MAT_Experiment_Glow"],
        "Wire": "MAT_Dark_Metal",
        "ToolRack": "MAT_Wood_Workbench",
        "Hook": "MAT_Dark_Metal",
        "Tool": "MAT_Tool_Steel",
    }

    for obj in objects:
        if not hasattr(obj, "name"):
            continue

        for key, mat_name in material_map.items():
            if key in obj.name:
                if isinstance(mat_name, list):
                    # Use hash of name for consistent selection
                    idx = hash(obj.name) % len(mat_name)
                    actual_mat = mat_name[idx]
                else:
                    actual_mat = mat_name

                if actual_mat in materials:
                    if obj.data and hasattr(obj.data, "materials"):
                        obj.data.materials.append(materials[actual_mat])
                break


# ============================================================
# COLLECTION
# ============================================================


def setup_collection():
    """Create and setup collection."""
    col_name = "Discovery_Zone"

    if col_name in bpy.data.collections:
        col = bpy.data.collections[col_name]
    else:
        col = bpy.data.collections.new(col_name)
        bpy.context.scene.collection.children.link(col)

    return col


def link_to_collection(obj, collection):
    """Link object to collection."""
    if obj is None:
        return

    collection.objects.link(obj)
    if obj.name in bpy.context.scene.collection.objects:
        bpy.context.scene.collection.objects.unlink(obj)


# ============================================================
# MAIN EXECUTION
# ============================================================


def main():
    """Main execution function."""
    print("=" * 50)
    print("MVXWorld — Discovery / Experiment Zone")
    print("=" * 50)

    # Setup collection
    col = setup_collection()

    # Get materials
    materials = get_materials()

    all_objects = []

    # Create workbench
    print("\n[1/7] Creating workbench...")
    bench_parts = create_workbench()
    all_objects.extend(bench_parts)

    # Create floating objects
    print("[2/7] Creating floating geometric objects...")
    floating_parts = create_floating_objects()
    all_objects.extend(floating_parts)

    # Create inventions
    print("[3/7] Creating half-finished inventions...")
    invention_parts = create_inventions()
    all_objects.extend(invention_parts)

    # Create devices
    print("[4/7] Creating abstract devices...")
    device_parts = create_devices()
    all_objects.extend(device_parts)

    # Create mechanisms
    print("[5/7] Creating physics mechanisms...")
    mechanism_parts = create_mechanisms()
    all_objects.extend(mechanism_parts)

    # Create suspended forms
    print("[6/7] Creating suspended forms...")
    suspended_parts = create_suspended_forms()
    all_objects.extend(suspended_parts)

    # Create tool rack
    print("[7/7] Creating tool rack...")
    tool_parts = create_tool_rack()
    all_objects.extend(tool_parts)

    # Create lighting
    print("\n[LIGHTS] Creating zone lighting...")
    light_parts = create_lighting()
    all_objects.extend(light_parts)

    # Apply materials
    print("[MATERIALS] Applying materials...")
    apply_materials(all_objects, materials)

    # Link to collection
    for obj in all_objects:
        link_to_collection(obj, col)

    # Deselect all
    bpy.ops.object.select_all(action="DESELECT")

    print("\n" + "=" * 50)
    print("DISCOVERY ZONE COMPLETE")
    print("=" * 50)
    print(f"\nTotal objects: {len(all_objects)}")
    print("\nComponents:")
    print("  - Experiment workbench")
    print("  - Floating geometric objects (8)")
    print("  - Half-finished inventions (3)")
    print("  - Abstract devices (4)")
    print("  - Physics mechanisms (2)")
    print("  - Suspended forms (5)")
    print("  - Tool rack + tools (10)")
    print("  - Zone lighting")
    print("\nMaterials applied:")
    print("  - Wood workbench")
    print("  - Dark metal (structure)")
    print("  - Brass antique (accents)")
    print("  - Crystal glass (transparent)")
    print("  - Copper patina (active project)")
    print("  - Experiment glow (emissive)")
    print("  - Tool steel (implements)")
    print("\nNext steps:")
    print("1. Add animation to floating objects")
    print("2. Create device interaction states")
    print("3. Add particle effects")
    print("4. Test lighting mood")


if __name__ == "__main__":
    main()
