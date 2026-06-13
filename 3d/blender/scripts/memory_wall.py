"""
MVXWorld — Memory Archive Wall
Run in Blender 4.0+ after graybox is loaded.

Usage:
1. Open MVXWorld_Room.blend
2. Switch to Scripting workspace
3. Open this file or paste contents
4. Click "Run Script"

Generates:
- Wall-mounted frame system (16 frames)
- Frame content placeholders
- Symbolic markings
- Wall lighting strips
"""

import bpy
import math
from mathutils import Vector, noise

# ============================================================
# CONFIGURATION
# ============================================================

WALL = {
    "width": 8.0,
    "height": 3.5,
    "y_pos": -5.0,  # North wall position
}

FRAMES = {
    "count": 16,
    "sizes": [
        (0.4, 0.3),
        (0.5, 0.4),
        (0.3, 0.4),
        (0.6, 0.5),
        (0.4, 0.6),
        (0.3, 0.3),
        (0.5, 0.3),
        (0.7, 0.5),
        (0.4, 0.4),
        (0.3, 0.5),
        (0.6, 0.4),
        (0.4, 0.3),
        (0.5, 0.5),
        (0.3, 0.4),
        (0.4, 0.6),
        (0.5, 0.3),
    ],
    "depth_offset": 0.05,  # How far frames are recessed into wall
    "frame_thickness": 0.03,
    "frame_depth": 0.02,
    "gap_min": 0.15,
    "gap_max": 0.35,
}

LIGHTING = {
    "strip_width": 0.02,
    "strip_intensity": 200,  # lumens per meter
    "color_temp": (1.0, 0.95, 0.9),  # 3000K warm
}

SYMBOLS = {
    "circle_dot": {
        "radius": 0.08,
        "dot_radius": 0.015,
    },
    "parallel_lines": {
        "count": 3,
        "spacing": 0.02,
        "length": 0.15,
    },
    "broken_circle": {
        "radius": 0.06,
        "gap_angle": 45,  # degrees
    },
}

# ============================================================
# UTILITIES
# ============================================================


def clean_name(prefix, name):
    """Create clean object name."""
    return f"MESH_{prefix}_{name}"


def create_material(name, color, roughness=0.7, metallic=0.0):
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

    return mat


def add_bevel(obj, width=0.003, segments=2):
    """Add bevel modifier."""
    bevel = obj.modifiers.new(name="Bevel", type="BEVEL")
    bevel.width = width
    bevel.segments = segments
    bevel.limit_method = "ANGLE"
    bevel.angle_limit = math.radians(30)
    return bevel


# ============================================================
# FRAME GENERATION
# ============================================================


def generate_frame_positions():
    """Generate organic frame layout positions."""
    positions = []

    # Define zones on the wall
    zones = [
        # (x_start, x_end, y_start, y_end)
        (-3.5, -1.5, 0.5, 2.8),  # Left cluster
        (-1.0, 1.0, 0.8, 3.0),  # Center cluster
        (1.5, 3.5, 0.5, 2.5),  # Right cluster
    ]

    for i, (w, h) in enumerate(FRAMES["sizes"]):
        # Pick zone based on frame index
        zone_idx = i % len(zones)
        x_start, x_end, y_start, y_end = zones[zone_idx]

        # Random position within zone
        x = x_start + (noise.random() * (x_end - x_start))
        y = y_start + (noise.random() * (y_end - y_start))

        # Ensure frame doesn't go outside wall
        x = max(x_start + w / 2, min(x_end - w / 2, x))
        y = max(y_start + h / 2, min(y_end - h / 2, y))

        # Random slight rotation (max 3 degrees)
        rotation = (noise.random() - 0.5) * 6

        positions.append(
            {
                "pos": (x, y),
                "size": (w, h),
                "rotation": rotation,
            }
        )

    return positions


def create_frame(name, position, size, rotation=0):
    """Create a single frame."""
    # Frame outer
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(position[0], WALL["y_pos"] + FRAMES["depth_offset"], position[1]),
    )
    frame = bpy.context.active_object
    frame.name = clean_name("Frame", f"{name}_Outer")
    frame.scale = (
        size[0] + FRAMES["frame_thickness"] * 2,
        FRAMES["frame_depth"],
        size[1] + FRAMES["frame_thickness"] * 2,
    )
    frame.rotation_euler[1] = math.radians(rotation)
    bpy.ops.object.transform_apply(scale=True)
    add_bevel(frame, width=0.002)

    # Frame inner (recessed)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(
            position[0],
            WALL["y_pos"] + FRAMES["depth_offset"] - 0.005,
            position[1],
        ),
    )
    inner = bpy.context.active_object
    inner.name = clean_name("Frame", f"{name}_Inner")
    inner.scale = (size[0], 0.01, size[1])
    inner.rotation_euler[1] = math.radians(rotation)
    bpy.ops.object.transform_apply(scale=True)

    # Content placeholder (canvas/surface)
    bpy.ops.mesh.primitive_plane_add(
        size=1,
        location=(
            position[0],
            WALL["y_pos"] + FRAMES["depth_offset"] - 0.008,
            position[1],
        ),
    )
    content = bpy.context.active_object
    content.name = clean_name("Frame", f"{name}_Content")
    content.scale = (size[0] * 0.95, size[1] * 0.95, 1)
    content.rotation_euler[0] = math.radians(90)
    content.rotation_euler[2] = math.radians(rotation)
    bpy.ops.object.transform_apply(scale=True, rotation=True)

    return [frame, inner, content]


# ============================================================
# SYMBOLS
# ============================================================


def create_circle_dot(position, name):
    """Create circle-with-dot symbol."""
    # Outer circle
    bpy.ops.mesh.primitive_torus_add(
        major_radius=SYMBOLS["circle_dot"]["radius"],
        minor_radius=0.005,
        location=(position[0], WALL["y_pos"] + 0.01, position[1]),
    )
    circle = bpy.context.active_object
    circle.name = clean_name("Symbol", f"Circle_{name}")
    circle.rotation_euler[0] = math.radians(90)

    # Center dot
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=SYMBOLS["circle_dot"]["dot_radius"],
        location=(position[0], WALL["y_pos"] + 0.012, position[1]),
    )
    dot = bpy.context.active_object
    dot.name = clean_name("Symbol", f"Dot_{name}")

    return [circle, dot]


def create_parallel_lines(position, name):
    """Create parallel lines symbol."""
    lines = []

    for i in range(SYMBOLS["parallel_lines"]["count"]):
        offset = (i - 1) * SYMBOLS["parallel_lines"]["spacing"]

        bpy.ops.mesh.primitive_cube_add(
            size=1, location=(position[0], WALL["y_pos"] + 0.01, position[1] + offset)
        )
        line = bpy.context.active_object
        line.name = clean_name("Symbol", f"Line_{name}_{i}")
        line.scale = (SYMBOLS["parallel_lines"]["length"], 0.003, 0.003)
        bpy.ops.object.transform_apply(scale=True)

        lines.append(line)

    return lines


def create_broken_circle(position, name):
    """Create broken circle symbol."""
    # Create full circle then delete a segment
    bpy.ops.mesh.primitive_circle_add(
        radius=SYMBOLS["broken_circle"]["radius"],
        vertices=64,
        location=(position[0], WALL["y_pos"] + 0.01, position[1]),
    )
    circle = bpy.context.active_object
    circle.name = clean_name("Symbol", f"BrokenCircle_{name}")

    # Convert to mesh and delete segment
    bpy.ops.object.convert(target="MESH")
    bpy.ops.object.mode_set(mode="EDIT")

    bm = bmesh.from_edit_data(circle.data)

    # Find vertices in the gap angle and delete them
    gap_start = math.radians(90 - SYMBOLS["broken_circle"]["gap_angle"] / 2)
    gap_end = math.radians(90 + SYMBOLS["broken_circle"]["gap_angle"] / 2)

    verts_to_delete = []
    for v in bm.verts:
        angle = math.atan2(v.co.y, v.co.x)
        if gap_start <= angle <= gap_end:
            verts_to_delete.append(v)

    bmesh.ops.delete(bm, geom=verts_to_delete, context="VERTS")

    bm.to_mesh(circle.data)
    bm.free()

    bpy.ops.object.mode_set(mode="OBJECT")

    # Add thickness
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0.01, 0)})
    bpy.ops.object.mode_set(mode="OBJECT")

    return [circle]


# ============================================================
# WALL LIGHTING
# ============================================================


def create_wall_lighting():
    """Create wall-mounted lighting strips."""
    lights = []

    # Horizontal light strip (behind frames)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, WALL["y_pos"] + 0.15, 1.5))
    strip_main = bpy.context.active_object
    strip_main.name = clean_name("Light", "Strip_Main")
    strip_main.scale = (7.0, LIGHTING["strip_width"], 0.01)
    bpy.ops.object.transform_apply(scale=True)

    # Create emissive material
    mat = create_material("MAT_Wall_Light", LIGHTING["color_temp"], roughness=0.2)
    mat.node_tree.nodes["Principled BSDF"].inputs["Emission Color"].default_value = (
        *LIGHTING["color_temp"],
        1,
    )
    mat.node_tree.nodes["Principled BSDF"].inputs[
        "Emission Strength"
    ].default_value = 3.0
    strip_main.data.materials.append(mat)

    lights.append(strip_main)

    # Spot lights for key frames
    spot_positions = [(-2.0, 2.0), (0, 2.5), (2.0, 2.0)]

    for i, (x, y) in enumerate(spot_positions):
        bpy.ops.object.light_add(
            type="SPOT", location=(x, WALL["y_pos"] + 0.3, y + 0.5)
        )
        spot = bpy.context.active_object
        spot.name = clean_name("Light", f"Spot_{i}")
        spot.data.energy = 500
        spot.data.color = LIGHTING["color_temp"]
        spot.data.spot_size = math.radians(45)
        spot.data.spot_blend = 0.5

        # Point at wall
        spot.rotation_euler[0] = math.radians(-70)

        lights.append(spot)

    return lights


# ============================================================
# MARKINGS AND DECALS
# ============================================================


def create_wall_markings():
    """Create symbolic markings on wall."""
    markings = []

    # Coordinates (etched into wall)
    coord_text = "52.3676° N · 4.9041° E"

    bpy.ops.object.text_add(location=(-3.0, WALL["y_pos"] + 0.02, 0.3))
    text_obj = bpy.context.active_object
    text_obj.name = clean_name("Marking", "Coordinates")
    text_obj.data.body = coord_text
    text_obj.data.size = 0.05
    text_obj.data.font = bpy.data.fonts["Bfont Regular"]
    text_obj.rotation_euler[0] = math.radians(90)

    # Convert to mesh
    bpy.ops.object.convert(target="MESH")

    markings.append(text_obj)

    # Random hash marks
    hash_positions = [(-1.5, 0.8), (2.5, 1.2), (-0.5, 2.8), (1.8, 0.6)]

    for i, (x, y) in enumerate(hash_positions):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, WALL["y_pos"] + 0.015, y))
        mark = bpy.context.active_object
        mark.name = clean_name("Marking", f"Hash_{i}")
        mark.scale = (0.08, 0.003, 0.003)
        mark.rotation_euler[2] = math.radians(noise.random() * 30 - 15)
        bpy.ops.object.transform_apply(scale=True, rotation=True)

        markings.append(mark)

    return markings


# ============================================================
# MATERIALS
# ============================================================


def get_materials():
    """Get or create all materials."""
    materials = {
        "MAT_Frame_Dark": create_material(
            "MAT_Frame_Dark", (0.08, 0.08, 0.07), roughness=0.60, metallic=0.1
        ),
        "MAT_Frame_Wood": create_material(
            "MAT_Frame_Wood", (0.25, 0.18, 0.12), roughness=0.70, metallic=0.0
        ),
        "MAT_Canvas": create_material(
            "MAT_Canvas", (0.92, 0.90, 0.85), roughness=0.95, metallic=0.0
        ),
        "MAT_Paper_Old": create_material(
            "MAT_Paper_Old", (0.88, 0.84, 0.78), roughness=0.90, metallic=0.0
        ),
        "MAT_Photo": create_material(
            "MAT_Photo", (0.75, 0.72, 0.68), roughness=0.85, metallic=0.0
        ),
        "MAT_Wall_Surface": create_material(
            "MAT_Wall_Surface", (0.10, 0.10, 0.09), roughness=0.80, metallic=0.0
        ),
        "MAT_Symbol_Etched": create_material(
            "MAT_Symbol_Etched", (0.15, 0.15, 0.14), roughness=0.60, metallic=0.0
        ),
    }

    return materials


def apply_materials(objects, materials):
    """Apply materials to objects."""
    material_map = {
        "Outer": "MAT_Frame_Dark",
        "Inner": "MAT_Frame_Wood",
        "Content": ["MAT_Canvas", "MAT_Paper_Old", "MAT_Photo"],
        "Symbol": "MAT_Symbol_Etched",
        "Marking": "MAT_Symbol_Etched",
    }

    content_idx = 0

    for obj in objects:
        applied = False

        for key, mat_name in material_map.items():
            if key in obj.name:
                if isinstance(mat_name, list):
                    # Cycle through content materials
                    actual_mat = mat_name[content_idx % len(mat_name)]
                    content_idx += 1
                else:
                    actual_mat = mat_name

                if actual_mat in materials:
                    obj.data.materials.append(materials[actual_mat])
                applied = True
                break

        if not applied and "Light" not in obj.name:
            # Default material
            if "MAT_Wall_Surface" in materials:
                obj.data.materials.append(materials["MAT_Wall_Surface"])


# ============================================================
# COLLECTION
# ============================================================


def setup_collection():
    """Create and setup collection."""
    col_name = "Memory_Wall"

    if col_name in bpy.data.collections:
        col = bpy.data.collections[col_name]
    else:
        col = bpy.data.collections.new(col_name)
        bpy.context.scene.collection.children.link(col)

    return col


def link_to_collection(obj, collection):
    """Link object to collection."""
    collection.objects.link(obj)
    if obj.name in bpy.context.scene.collection.objects:
        bpy.context.scene.collection.objects.unlink(obj)


# ============================================================
# MAIN EXECUTION
# ============================================================


def main():
    """Main execution function."""
    print("=" * 50)
    print("MVXWorld — Memory Archive Wall")
    print("=" * 50)

    # Setup collection
    col = setup_collection()

    # Get materials
    materials = get_materials()

    all_objects = []

    # Generate frame positions
    print("\n[1/5] Generating frame layout...")
    positions = generate_frame_positions()

    # Create frames
    print("[2/5] Creating frames...")
    for i, pos_data in enumerate(positions):
        frame_parts = create_frame(
            f"Frame_{i:02d}", pos_data["pos"], pos_data["size"], pos_data["rotation"]
        )
        all_objects.extend(frame_parts)

    # Create symbols
    print("[3/5] Creating symbols...")

    # Circle-dot symbols (3 instances)
    symbol_positions = [(-2.0, 1.5), (0.5, 2.2), (2.5, 1.0)]
    for i, pos in enumerate(symbol_positions):
        symbols = create_circle_dot(pos, f"CircleDot_{i}")
        all_objects.extend(symbols)

    # Parallel lines (2 instances)
    line_positions = [(-1.0, 0.8), (1.5, 2.5)]
    for i, pos in enumerate(line_positions):
        lines = create_parallel_lines(pos, f"Lines_{i}")
        all_objects.extend(lines)

    # Broken circles (2 instances)
    broken_positions = [(-3.0, 2.0), (3.0, 1.8)]
    for i, pos in enumerate(broken_positions):
        broken = create_broken_circle(pos, f"Broken_{i}")
        all_objects.extend(broken)

    # Create wall lighting
    print("[4/5] Creating wall lighting...")
    lights = create_wall_lighting()
    all_objects.extend(lights)

    # Create markings
    print("[5/5] Creating wall markings...")
    markings = create_wall_markings()
    all_objects.extend(markings)

    # Apply materials
    print("\n[MATERIALS] Applying materials...")
    apply_materials(all_objects, materials)

    # Link to collection
    for obj in all_objects:
        link_to_collection(obj, col)

    # Deselect all
    bpy.ops.object.select_all(action="DESELECT")

    print("\n" + "=" * 50)
    print("MEMORY WALL COMPLETE")
    print("=" * 50)
    print(f"\nTotal objects: {len(all_objects)}")
    print("\nComponents:")
    print(f"  - {len(positions)} floating frames")
    print("  - 3 circle-dot symbols")
    print("  - 2 parallel line groups")
    print("  - 2 broken circles")
    print("  - Wall lighting strip")
    print("  - 3 spot lights")
    print("  - Coordinate markings")
    print("  - Hash marks")
    print("\nStory elements hidden:")
    print("  - Amsterdam coordinates (52.3676° N · 4.9041° E)")
    print("  - Recurring symbols across frames")
    print("  - Etched hash marks with slight rotation")
    print("\nNext steps:")
    print("1. Add actual frame content (images/textures)")
    print("2. Create distortion shader for old photos")
    print("3. Add dust particles near frames")
    print("4. Test lighting mood")


if __name__ == "__main__":
    main()
