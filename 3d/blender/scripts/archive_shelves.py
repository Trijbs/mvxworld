"""
MVXWorld — Archive Shelves
Run in Blender 4.0+ after graybox is loaded.

Usage:
1. Open MVXWorld_Room.blend
2. Switch to Scripting workspace
3. Open this file or paste contents
4. Click "Run Script"

Generates:
- 3 modular shelving units
- Books (30 instances)
- Journals (8 instances)
- Physical artifacts (12 instances)
- Miniature world models (4 instances)
- Specimen jars (3 instances)
- Shelf lighting
"""

import bpy
import math
from mathutils import Vector, noise

# ============================================================
# CONFIGURATION
# ============================================================

ZONE = {
    "center": (-3.5, -2.0, 0),
    "size": (3.0, 0.6),
}

SHELVING = {
    "unit_width": 0.9,
    "unit_depth": 0.35,
    "unit_height": 2.2,
    "shelf_thickness": 0.025,
    "frame_thickness": 0.04,
    "shelf_count": 4,
    "spacing": 0.15,
}

BOOKS = {
    "count": 30,
    "min_height": 0.18,
    "max_height": 0.28,
    "min_thickness": 0.015,
    "max_thickness": 0.04,
    "depth": 0.15,
}

JOURNALS = {
    "count": 8,
    "size": (0.2, 0.03, 0.28),
}

ARTIFACTS = {
    "count": 12,
    "max_size": 0.12,
}

MINIATURES = {
    "count": 4,
    "base_size": 0.1,
    "max_height": 0.15,
}

JARS = {
    "count": 3,
    "radius": 0.04,
    "height": 0.12,
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


def add_bevel(obj, width=0.002, segments=2):
    """Add bevel modifier."""
    bevel = obj.modifiers.new(name="Bevel", type="BEVEL")
    bevel.width = width
    bevel.segments = segments
    bevel.limit_method = "ANGLE"
    bevel.angle_limit = math.radians(30)
    return bevel


# ============================================================
# SHELVING UNITS
# ============================================================


def create_shelving_unit(position, unit_index):
    """Create a single shelving unit."""
    x, y, z = position
    parts = []

    # Side panels
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(
                x
                + side * (SHELVING["unit_width"] / 2 - SHELVING["frame_thickness"] / 2),
                y,
                z + SHELVING["unit_height"] / 2,
            ),
        )
        panel = bpy.context.active_object
        panel.name = clean_name("Shelf", f"Unit_{unit_index}_Side_{side}")
        panel.scale = (
            SHELVING["frame_thickness"],
            SHELVING["unit_depth"],
            SHELVING["unit_height"],
        )
        bpy.ops.object.transform_apply(scale=True)
        add_bevel(panel, width=0.003)
        parts.append(panel)

    # Back panel
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(
            x,
            y - SHELVING["unit_depth"] / 2 + SHELVING["frame_thickness"] / 2,
            z + SHELVING["unit_height"] / 2,
        ),
    )
    back = bpy.context.active_object
    back.name = clean_name("Shelf", f"Unit_{unit_index}_Back")
    back.scale = (
        SHELVING["unit_width"],
        SHELVING["frame_thickness"],
        SHELVING["unit_height"],
    )
    bpy.ops.object.transform_apply(scale=True)
    parts.append(back)

    # Shelves
    for i in range(SHELVING["shelf_count"]):
        shelf_z = z + 0.05 + i * (SHELVING["unit_height"] / SHELVING["shelf_count"])

        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, shelf_z))
        shelf = bpy.context.active_object
        shelf.name = clean_name("Shelf", f"Unit_{unit_index}_Shelf_{i}")
        shelf.scale = (
            SHELVING["unit_width"],
            SHELVING["unit_depth"],
            SHELVING["shelf_thickness"],
        )
        bpy.ops.object.transform_apply(scale=True)
        add_bevel(shelf, width=0.002)
        parts.append(shelf)

    # Top
    bpy.ops.mesh.primitive_cube_add(
        size=1, location=(x, y, z + SHELVING["unit_height"])
    )
    top = bpy.context.active_object
    top.name = clean_name("Shelf", f"Unit_{unit_index}_Top")
    top.scale = (
        SHELVING["unit_width"] + 0.02,
        SHELVING["unit_depth"] + 0.01,
        SHELVING["shelf_thickness"],
    )
    bpy.ops.object.transform_apply(scale=True)
    add_bevel(top, width=0.003)
    parts.append(top)

    return parts


# ============================================================
# BOOKS
# ============================================================


def create_book(position, size, book_index):
    """Create a single book."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=position)
    book = bpy.context.active_object
    book.name = clean_name("Book", f"{book_index:02d}")
    book.scale = size
    book.rotation_euler[2] = math.radians(noise.random() * 4 - 2)  # Slight lean
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    add_bevel(book, width=0.001)

    return book


def create_book_collection(shelf_position, shelf_index, count=8):
    """Create a collection of books on a shelf."""
    x, y, z = shelf_position
    books = []

    current_x = x - SHELVING["unit_width"] / 2 + 0.05

    for i in range(count):
        # Random book dimensions
        height = BOOKS["min_height"] + noise.random() * (
            BOOKS["max_height"] - BOOKS["min_height"]
        )
        thickness = BOOKS["min_thickness"] + noise.random() * (
            BOOKS["max_thickness"] - BOOKS["min_thickness"]
        )

        book_x = current_x + thickness / 2
        book_y = y + 0.02
        book_z = z + height / 2 + SHELVING["shelf_thickness"] / 2

        book = create_book(
            (book_x, book_y, book_z),
            (thickness, BOOKS["depth"], height),
            shelf_index * 100 + i,
        )
        books.append(book)

        current_x += thickness + 0.002  # Small gap

    return books


# ============================================================
# JOURNALS
# ============================================================


def create_journal(position, journal_index):
    """Create a leather-bound journal."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=position)
    journal = bpy.context.active_object
    journal.name = clean_name("Journal", f"{journal_index:02d}")
    journal.scale = JOURNALS["size"]
    journal.rotation_euler[2] = math.radians(noise.random() * 10 - 5)
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    add_bevel(journal, width=0.003)

    return journal


# ============================================================
# ARTIFACTS
# ============================================================


def create_artifact(position, artifact_index):
    """Create an unknown artifact."""
    artifact_type = artifact_index % 4

    if artifact_type == 0:
        # Irregular stone
        bpy.ops.mesh.primitive_ico_sphere_add(
            radius=ARTIFACTS["max_size"] / 2, location=position, subdivisions=2
        )
        obj = bpy.context.active_object
        obj.name = clean_name("Artifact", f"Stone_{artifact_index:02d}")
        obj.scale[0] *= 1.2
        obj.scale[1] *= 0.8
        obj.scale[2] *= 0.9

    elif artifact_type == 1:
        # Cylinder artifact
        bpy.ops.mesh.primitive_cylinder_add(
            radius=ARTIFACTS["max_size"] / 3,
            depth=ARTIFACTS["max_size"],
            location=position,
        )
        obj = bpy.context.active_object
        obj.name = clean_name("Artifact", f"Cylinder_{artifact_index:02d}")

    elif artifact_type == 2:
        # Pyramid
        bpy.ops.mesh.primitive_cone_add(
            radius1=ARTIFACTS["max_size"] / 2,
            radius2=0,
            depth=ARTIFACTS["max_size"],
            location=position,
        )
        obj = bpy.context.active_object
        obj.name = clean_name("Artifact", f"Pyramid_{artifact_index:02d}")

    else:
        # Torus fragment
        bpy.ops.mesh.primitive_torus_add(
            major_radius=ARTIFACTS["max_size"] / 2,
            minor_radius=ARTIFACTS["max_size"] / 6,
            location=position,
        )
        obj = bpy.context.active_object
        obj.name = clean_name("Artifact", f"Torus_{artifact_index:02d}")

    obj.rotation_euler[0] = math.radians(noise.random() * 30)
    obj.rotation_euler[1] = math.radians(noise.random() * 30)
    obj.rotation_euler[2] = math.radians(noise.random() * 360)
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    add_bevel(obj, width=0.002)

    return obj


# ============================================================
# MINIATURE WORLD MODELS
# ============================================================


def create_miniature(position, model_index):
    """Create a miniature world model."""
    bpy.ops.mesh.primitive_cylinder_add(
        radius=MINIATURES["base_size"] / 2, depth=0.005, location=position
    )
    base = bpy.context.active_object
    base.name = clean_name("Miniature", f"Base_{model_index}")

    # Abstract structure on top
    structure_type = model_index % 3

    if structure_type == 0:
        # Tower
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.02,
            depth=MINIATURES["max_height"],
            location=(
                position[0],
                position[1],
                position[2] + MINIATURES["max_height"] / 2,
            ),
        )
        structure = bpy.context.active_object
        structure.name = clean_name("Miniature", f"Tower_{model_index}")

    elif structure_type == 1:
        # Arch
        bpy.ops.mesh.primitive_torus_add(
            major_radius=0.04,
            minor_radius=0.008,
            location=(position[0], position[1], position[2] + 0.04),
        )
        structure = bpy.context.active_object
        structure.name = clean_name("Miniature", f"Arch_{model_index}")
        structure.rotation_euler[0] = math.radians(90)

    else:
        # Sphere cluster
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.03, location=(position[0], position[1], position[2] + 0.03)
        )
        structure = bpy.context.active_object
        structure.name = clean_name("Miniature", f"Sphere_{model_index}")

    bpy.ops.object.transform_apply(scale=True, rotation=True)

    return [base, structure]


# ============================================================
# SPECIMEN JARS
# ============================================================


def create_specimen_jar(position, jar_index):
    """Create a specimen jar with contents."""
    x, y, z = position

    # Jar body (glass)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=JARS["radius"],
        depth=JARS["height"],
        location=(x, y, z + JARS["height"] / 2),
    )
    jar = bpy.context.active_object
    jar.name = clean_name("Jar", f"Body_{jar_index}")

    # Jar lid
    bpy.ops.mesh.primitive_cylinder_add(
        radius=JARS["radius"] + 0.005,
        depth=0.01,
        location=(x, y, z + JARS["height"] + 0.005),
    )
    lid = bpy.context.active_object
    lid.name = clean_name("Jar", f"Lid_{jar_index}")

    # Contents (mysterious)
    bpy.ops.mesh.primitive_ico_sphere_add(
        radius=JARS["radius"] * 0.6,
        location=(x, y, z + JARS["height"] * 0.4),
        subdivisions=2,
    )
    contents = bpy.context.active_object
    contents.name = clean_name("Jar", f"Contents_{jar_index}")
    contents.scale[2] *= 0.7
    bpy.ops.object.transform_apply(scale=True)

    return [jar, lid, contents]


# ============================================================
# LIGHTING
# ============================================================


def create_lighting():
    """Create shelf lighting."""
    x, y, z = ZONE["center"]
    parts = []

    # Shelf strip lights
    for i in range(3):
        unit_x = x - 0.6 + i * 0.6

        bpy.ops.mesh.primitive_cube_add(
            size=1, location=(unit_x, y + 0.15, z + SHELVING["unit_height"] - 0.05)
        )
        strip = bpy.context.active_object
        strip.name = clean_name("Light", f"Strip_{i}")
        strip.scale = (SHELVING["unit_width"] * 0.8, 0.01, 0.005)
        bpy.ops.object.transform_apply(scale=True)
        parts.append(strip)

    # Ambient spot
    bpy.ops.object.light_add(type="SPOT", location=(x, y + 0.5, z + 2.5))
    spot = bpy.context.active_object
    spot.name = clean_name("Light", "ArchiveAmbient")
    spot.data.energy = 500
    spot.data.color = (0.95, 0.92, 0.85)  # Warm
    spot.data.spot_size = math.radians(90)
    spot.rotation_euler[0] = math.radians(-60)
    parts.append(spot)

    return parts


# ============================================================
# MATERIALS
# ============================================================


def get_materials():
    """Get or create all materials."""
    materials = {
        "MAT_Walnut_Dark": create_material(
            "MAT_Walnut_Dark", (0.18, 0.12, 0.08), roughness=0.75, metallic=0.0
        ),
        "MAT_Brushed_Metal": create_material(
            "MAT_Brushed_Metal", (0.50, 0.50, 0.48), roughness=0.50, metallic=0.85
        ),
        "MAT_Book_Red": create_material(
            "MAT_Book_Red", (0.45, 0.08, 0.06), roughness=0.70, metallic=0.0
        ),
        "MAT_Book_Blue": create_material(
            "MAT_Book_Blue", (0.08, 0.12, 0.35), roughness=0.70, metallic=0.0
        ),
        "MAT_Book_Green": create_material(
            "MAT_Book_Green", (0.08, 0.25, 0.12), roughness=0.70, metallic=0.0
        ),
        "MAT_Book_Brown": create_material(
            "MAT_Book_Brown", (0.30, 0.18, 0.10), roughness=0.70, metallic=0.0
        ),
        "MAT_Leather_Dark": create_material(
            "MAT_Leather_Dark", (0.12, 0.08, 0.05), roughness=0.60, metallic=0.0
        ),
        "MAT_Stone_Gray": create_material(
            "MAT_Stone_Gray", (0.35, 0.34, 0.32), roughness=0.80, metallic=0.0
        ),
        "MAT_Glass_Tinted": create_material(
            "MAT_Glass_Tinted", (0.85, 0.90, 0.88), roughness=0.05, metallic=0.0
        ),
        "MAT_Jar_Contents": create_material(
            "MAT_Jar_Contents", (0.2, 0.5, 0.3), roughness=0.30, metallic=0.0
        ),
        "MAT_Light_Warm": create_material(
            "MAT_Light_Warm", (1.0, 0.92, 0.8), roughness=0.10, metallic=0.0
        ),
    }

    # Add emission to light material
    light_mat = materials["MAT_Light_Warm"]
    light_mat.node_tree.nodes["Principled BSDF"].inputs[
        "Emission Color"
    ].default_value = (1.0, 0.92, 0.8, 1)
    light_mat.node_tree.nodes["Principled BSDF"].inputs[
        "Emission Strength"
    ].default_value = 2.0

    return materials


def apply_materials(objects, materials):
    """Apply materials to objects."""
    book_colors = ["MAT_Book_Red", "MAT_Book_Blue", "MAT_Book_Green", "MAT_Book_Brown"]

    for obj in objects:
        if not hasattr(obj, "name"):
            continue

        if "Book" in obj.name:
            # Cycle through book colors
            idx = int(obj.name.split("_")[-1]) if "_" in obj.name else 0
            mat_name = book_colors[idx % len(book_colors)]
            if mat_name in materials:
                obj.data.materials.append(materials[mat_name])

        elif "Journal" in obj.name:
            if "MAT_Leather_Dark" in materials:
                obj.data.materials.append(materials["MAT_Leather_Dark"])

        elif "Artifact" in obj.name or "Stone" in obj.name:
            if "MAT_Stone_Gray" in materials:
                obj.data.materials.append(materials["MAT_Stone_Gray"])

        elif "Miniature" in obj.name:
            if "MAT_Stone_Gray" in materials:
                obj.data.materials.append(materials["MAT_Stone_Gray"])

        elif "Jar_Body" in obj.name:
            if "MAT_Glass_Tinted" in materials:
                obj.data.materials.append(materials["MAT_Glass_Tinted"])

        elif "Jar_Lid" in obj.name:
            if "MAT_Brushed_Metal" in materials:
                obj.data.materials.append(materials["MAT_Brushed_Metal"])

        elif "Jar_Contents" in obj.name:
            if "MAT_Jar_Contents" in materials:
                obj.data.materials.append(materials["MAT_Jar_Contents"])

        elif (
            "Shelf" in obj.name
            or "Side" in obj.name
            or "Back" in obj.name
            or "Top" in obj.name
        ):
            if "MAT_Walnut_Dark" in materials:
                obj.data.materials.append(materials["MAT_Walnut_Dark"])

        elif "Light" in obj.name or "Strip" in obj.name:
            if "MAT_Light_Warm" in materials:
                obj.data.materials.append(materials["MAT_Light_Warm"])


# ============================================================
# COLLECTION
# ============================================================


def setup_collection():
    """Create and setup collection."""
    col_name = "Archive_Shelves"

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
    print("MVXWorld — Archive Shelves")
    print("=" * 50)

    # Setup collection
    col = setup_collection()

    # Get materials
    materials = get_materials()

    all_objects = []

    # Create shelving units
    print("\n[1/6] Creating shelving units...")
    x, y, z = ZONE["center"]

    for i in range(3):
        unit_x = x - 0.6 + i * 0.6
        unit_parts = create_shelving_unit((unit_x, y, z), i)
        all_objects.extend(unit_parts)

    # Create books
    print("[2/6] Creating books...")
    books_per_shelf = BOOKS["count"] // (3 * SHELVING["shelf_count"])

    for unit_idx in range(3):
        unit_x = x - 0.6 + unit_idx * 0.6

        for shelf_idx in range(SHELVING["shelf_count"]):
            shelf_z = (
                z
                + 0.05
                + shelf_idx * (SHELVING["unit_height"] / SHELVING["shelf_count"])
            )
            shelf_pos = (unit_x, y, shelf_z)

            books = create_book_collection(
                shelf_pos, unit_idx * 10 + shelf_idx, books_per_shelf
            )
            all_objects.extend(books)

    # Create journals
    print("[3/6] Creating journals...")
    for i in range(JOURNALS["count"]):
        unit_idx = i % 3
        shelf_idx = i // 3
        unit_x = x - 0.6 + unit_idx * 0.6
        shelf_z = (
            z
            + 0.05
            + shelf_idx * (SHELVING["unit_height"] / SHELVING["shelf_count"])
            + 0.05
        )

        journal = create_journal(
            (unit_x + 0.2, y + 0.02, shelf_z + JOURNALS["size"][2] / 2), i
        )
        all_objects.append(journal)

    # Create artifacts
    print("[4/6] Creating artifacts...")
    for i in range(ARTIFACTS["count"]):
        unit_idx = i % 3
        shelf_idx = (i // 3) % SHELVING["shelf_count"]
        unit_x = x - 0.6 + unit_idx * 0.6
        shelf_z = (
            z
            + 0.05
            + shelf_idx * (SHELVING["unit_height"] / SHELVING["shelf_count"])
            + 0.03
        )

        artifact = create_artifact(
            (unit_x - 0.2, y, shelf_z + ARTIFACTS["max_size"] / 2), i
        )
        all_objects.append(artifact)

    # Create miniature world models
    print("[5/6] Creating miniature world models...")
    for i in range(MINIATURES["count"]):
        unit_idx = i % 3
        shelf_idx = i // 3 + 1
        unit_x = x - 0.6 + unit_idx * 0.6
        shelf_z = (
            z
            + 0.05
            + shelf_idx * (SHELVING["unit_height"] / SHELVING["shelf_count"])
            + 0.01
        )

        mini_parts = create_miniature((unit_x + 0.1, y, shelf_z + 0.005), i)
        all_objects.extend(mini_parts)

    # Create specimen jars
    print("[6/6] Creating specimen jars...")
    for i in range(JARS["count"]):
        unit_idx = i
        shelf_idx = 2
        unit_x = x - 0.6 + unit_idx * 0.6
        shelf_z = (
            z + 0.05 + shelf_idx * (SHELVING["unit_height"] / SHELVING["shelf_count"])
        )

        jar_parts = create_specimen_jar(
            (unit_x - 0.1, y, shelf_z + SHELVING["shelf_thickness"] / 2), i
        )
        all_objects.extend(jar_parts)

    # Create lighting
    print("\n[LIGHTS] Creating shelf lighting...")
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
    print("ARCHIVE SHELVES COMPLETE")
    print("=" * 50)
    print(f"\nTotal objects: {len(all_objects)}")
    print("\nComponents:")
    print("  - 3 shelving units")
    print(f"  - {BOOKS['count']} books")
    print(f"  - {JOURNALS['count']} journals")
    print(f"  - {ARTIFACTS['count']} artifacts")
    print(f"  - {MINIATURES['count']} miniature world models")
    print(f"  - {JARS['count']} specimen jars")
    print("  - Shelf lighting")
    print("\nMaterials applied:")
    print("  - Walnut dark (shelving)")
    print("  - Book colors (red, blue, green, brown)")
    print("  - Leather dark (journals)")
    print("  - Stone gray (artifacts)")
    print("  - Tinted glass (jars)")
    print("  - Warm light (strips)")
    print("\nNext steps:")
    print("1. Add book spine textures")
    print("2. Create journal cover details")
    print("3. Add dust particles")
    print("4. Test shelf lighting")


if __name__ == "__main__":
    main()
