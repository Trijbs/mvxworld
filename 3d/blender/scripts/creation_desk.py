"""
MVXWorld — Creation Desk (Hero Asset)
Run in Blender 4.0+ after graybox is loaded.

Usage:
1. Open MVXWorld_Room.blend
2. Switch to Scripting workspace
3. Open this file or paste contents
4. Click "Run Script"

Generates:
- Main desk surface (aged walnut)
- Drawer units (left + right)
- Desk legs (brushed metal)
- Back panel with shelves
- Cable management
- Monitor arm mounts
- Detail props (coffee cup, pen holder)
"""

import bpy
import bmesh
from mathutils import Vector
import math

# ============================================================
# CONFIGURATION
# ============================================================

DESK = {
    "width": 1.8,  # meters
    "depth": 0.9,  # meters
    "height": 0.75,  # meters (surface height)
    "thickness": 0.04,  # surface thickness
    "edge_chamfer": 0.005,  # subtle edge softening
}

DRAWER = {
    "width": 0.5,
    "depth": 0.6,
    "height": 0.15,
    "count": 3,  # drawers per unit
    "gap": 0.01,  # gap between drawers
}

BACK_PANEL = {
    "width": 1.6,
    "height": 0.8,
    "thickness": 0.02,
    "shelf_depth": 0.25,
    "shelf_count": 2,
}

LEGS = {
    "diameter": 0.04,
    "height": 0.70,  # from floor to desk underside
    "style": "round",  # round or square
    "chamfer": 0.005,
}

MONITOR_ARM = {
    "pole_diameter": 0.03,
    "pole_height": 0.5,
    "arm_length": 0.4,
    "clamp_width": 0.08,
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


def add_bevel(obj, width=0.005, segments=3):
    """Add bevel modifier for edge softening."""
    bevel = obj.modifiers.new(name="Bevel", type="BEVEL")
    bevel.width = width
    bevel.segments = segments
    bevel.limit_method = "ANGLE"
    bevel.angle_limit = math.radians(30)
    return bevel


def add_subdivision(obj, levels=1):
    """Add subdivision surface for smoothness."""
    sub = obj.modifiers.new(name="Subdivision", type="SUBSURF")
    sub.levels = levels
    sub.render_levels = levels + 1
    return sub


# ============================================================
# DESK SURFACE
# ============================================================


def create_desk_surface():
    """Create main desk surface."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, DESK["height"]))
    surface = bpy.context.active_object
    surface.name = clean_name("Desk", "Surface")
    surface.scale = (DESK["width"], DESK["depth"], DESK["thickness"])
    bpy.ops.object.transform_apply(scale=True)

    # Add bevel for worn edges
    add_bevel(surface, width=DESK["edge_chamfer"], segments=2)

    return surface


# ============================================================
# DRAWER UNITS
# ============================================================


def create_drawer_unit(side="left"):
    """Create a drawer unit with multiple drawers."""
    unit_x = (
        -DESK["width"] / 2 + DRAWER["width"] / 2 + 0.05
        if side == "left"
        else DESK["width"] / 2 - DRAWER["width"] / 2 - 0.05
    )

    # Unit housing
    bpy.ops.mesh.primitive_cube_add(size=1, location=(unit_x, -0.1, DESK["height"] / 2))
    housing = bpy.context.active_object
    housing.name = clean_name("DrawerUnit", f"Housing_{side}")
    housing.scale = (
        DRAWER["width"],
        DRAWER["depth"],
        DESK["height"] - DESK["thickness"],
    )
    bpy.ops.object.transform_apply(scale=True)
    add_bevel(housing, width=0.003)

    drawers = []

    # Individual drawers
    for i in range(DRAWER["count"]):
        z = 0.05 + i * (DRAWER["height"] + DRAWER["gap"])

        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(
                unit_x,
                -0.1 - DRAWER["depth"] / 2 - 0.02,
                z + DRAWER["height"] / 2,
            ),
        )
        drawer = bpy.context.active_object
        drawer.name = clean_name("Drawer", f"{side}_{i}")
        drawer.scale = (DRAWER["width"] - 0.01, 0.02, DRAWER["height"] - 0.005)
        bpy.ops.object.transform_apply(scale=True)
        add_bevel(drawer, width=0.002)

        # Drawer handle
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.008,
            depth=DRAWER["width"] * 0.6,
            location=(
                unit_x,
                -0.1 - DRAWER["depth"] / 2 - 0.03,
                z + DRAWER["height"] / 2,
            ),
        )
        handle = bpy.context.active_object
        handle.name = clean_name("Drawer", f"Handle_{side}_{i}")
        handle.rotation_euler[1] = math.radians(90)

        drawers.append(drawer)
        drawers.append(handle)

    return housing, drawers


# ============================================================
# DESK LEGS
# ============================================================


def create_legs():
    """Create desk legs."""
    legs = []
    leg_positions = [
        (-DESK["width"] / 2 + 0.08, -DESK["depth"] / 2 + 0.08),
        (-DESK["width"] / 2 + 0.08, DESK["depth"] / 2 - 0.08),
        (DESK["width"] / 2 - 0.08, -DESK["depth"] / 2 + 0.08),
        (DESK["width"] / 2 - 0.08, DESK["depth"] / 2 - 0.08),
    ]

    for i, (x, y) in enumerate(leg_positions):
        bpy.ops.mesh.primitive_cylinder_add(
            radius=LEGS["diameter"] / 2,
            depth=LEGS["height"],
            location=(x, y, LEGS["height"] / 2),
        )
        leg = bpy.context.active_object
        leg.name = clean_name("Desk", f"Leg_{i}")

        # Add foot pad
        bpy.ops.mesh.primitive_cylinder_add(
            radius=LEGS["diameter"] / 2 + 0.01, depth=0.005, location=(x, y, 0.0025)
        )
        foot = bpy.context.active_object
        foot.name = clean_name("Desk", f"Foot_{i}")

        legs.extend([leg, foot])

    return legs


# ============================================================
# BACK PANEL + SHELVES
# ============================================================


def create_back_panel():
    """Create back panel with shelves."""
    panel_y = -DESK["depth"] / 2 + BACK_PANEL["thickness"] / 2

    # Main panel
    bpy.ops.mesh.primitive_cube_add(
        size=1, location=(0, panel_y, DESK["height"] + BACK_PANEL["height"] / 2)
    )
    panel = bpy.context.active_object
    panel.name = clean_name("BackPanel", "Main")
    panel.scale = (BACK_PANEL["width"], BACK_PANEL["thickness"], BACK_PANEL["height"])
    bpy.ops.object.transform_apply(scale=True)
    add_bevel(panel, width=0.003)

    shelves = []

    # Shelves
    for i in range(BACK_PANEL["shelf_count"]):
        z = DESK["height"] + 0.25 + i * 0.3

        bpy.ops.mesh.primitive_cube_add(
            size=1, location=(0, panel_y + BACK_PANEL["shelf_depth"] / 2, z)
        )
        shelf = bpy.context.active_object
        shelf.name = clean_name("BackPanel", f"Shelf_{i}")
        shelf.scale = (BACK_PANEL["width"] - 0.02, BACK_PANEL["shelf_depth"], 0.02)
        bpy.ops.object.transform_apply(scale=True)
        add_bevel(shelf, width=0.002)

        # Shelf brackets
        for bracket_x in [
            -BACK_PANEL["width"] / 2 + 0.1,
            BACK_PANEL["width"] / 2 - 0.1,
        ]:
            bpy.ops.mesh.primitive_cube_add(
                size=1, location=(bracket_x, panel_y + 0.02, z - 0.01)
            )
            bracket = bpy.context.active_object
            bracket.name = clean_name("BackPanel", f"Bracket_{i}_{bracket_x:.1f}")
            bracket.scale = (0.03, 0.04, 0.02)
            bpy.ops.object.transform_apply(scale=True)

            shelves.append(bracket)

        shelves.append(shelf)

    return panel, shelves


# ============================================================
# MONITOR ARM
# ============================================================


def create_monitor_arm():
    """Create monitor arm mount."""
    arm_x = 0.2  # Offset from center

    # Clamp base
    bpy.ops.mesh.primitive_cube_add(
        size=1, location=(arm_x, -DESK["depth"] / 2 + 0.05, DESK["height"] + 0.02)
    )
    clamp = bpy.context.active_object
    clamp.name = clean_name("MonitorArm", "Clamp")
    clamp.scale = (MONITOR_ARM["clamp_width"], 0.04, 0.04)
    bpy.ops.object.transform_apply(scale=True)
    add_bevel(clamp, width=0.002)

    # Pole
    bpy.ops.mesh.primitive_cylinder_add(
        radius=MONITOR_ARM["pole_diameter"] / 2,
        depth=MONITOR_ARM["pole_height"],
        location=(
            arm_x,
            -DESK["depth"] / 2 + 0.05,
            DESK["height"] + MONITOR_ARM["pole_height"] / 2,
        ),
    )
    pole = bpy.context.active_object
    pole.name = clean_name("MonitorArm", "Pole")

    # Arm
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.012,
        depth=MONITOR_ARM["arm_length"],
        location=(
            arm_x + MONITOR_ARM["arm_length"] / 2,
            -DESK["depth"] / 2 + 0.05,
            DESK["height"] + MONITOR_ARM["pole_height"],
        ),
    )
    arm = bpy.context.active_object
    arm.name = clean_name("MonitorArm", "Arm")
    arm.rotation_euler[2] = math.radians(90)

    # VESA mount
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(
            arm_x + MONITOR_ARM["arm_length"],
            -DESK["depth"] / 2 + 0.05,
            DESK["height"] + MONITOR_ARM["pole_height"],
        ),
    )
    vesa = bpy.context.active_object
    vesa.name = clean_name("MonitorArm", "VESA")
    vesa.scale = (0.1, 0.02, 0.1)
    bpy.ops.object.transform_apply(scale=True)

    return [clamp, pole, arm, vesa]


# ============================================================
# DETAIL PROPS
# ============================================================


def create_coffee_cup():
    """Create a coffee cup prop."""
    cup_x = DESK["width"] / 2 - 0.15
    cup_y = 0.1

    # Cup body
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.04, depth=0.08, location=(cup_x, cup_y, DESK["height"] + 0.04)
    )
    cup = bpy.context.active_object
    cup.name = clean_name("Props", "CoffeeCup")

    # Handle
    bpy.ops.mesh.primitive_torus_add(
        major_radius=0.025,
        minor_radius=0.005,
        location=(cup_x + 0.05, cup_y, DESK["height"] + 0.04),
    )
    handle = bpy.context.active_object
    handle.name = clean_name("Props", "CupHandle")
    handle.rotation_euler[1] = math.radians(90)

    # Coffee liquid (inside cup)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.035, depth=0.005, location=(cup_x, cup_y, DESK["height"] + 0.06)
    )
    coffee = bpy.context.active_object
    coffee.name = clean_name("Props", "Coffee")

    return [cup, handle, coffee]


def create_pen_holder():
    """Create a pen holder with pens."""
    holder_x = -DESK["width"] / 2 + 0.12
    holder_y = 0.15

    # Holder body
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.04, depth=0.1, location=(holder_x, holder_y, DESK["height"] + 0.05)
    )
    holder = bpy.context.active_object
    holder.name = clean_name("Props", "PenHolder")

    pens = []
    pen_colors = [(0.1, 0.1, 0.1), (0.2, 0.1, 0.05), (0.05, 0.05, 0.15)]

    for i, color in enumerate(pen_colors):
        angle = i * 30
        offset_x = math.cos(math.radians(angle)) * 0.02
        offset_y = math.sin(math.radians(angle)) * 0.02

        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.004,
            depth=0.15,
            location=(holder_x + offset_x, holder_y + offset_y, DESK["height"] + 0.1),
        )
        pen = bpy.context.active_object
        pen.name = clean_name("Props", f"Pen_{i}")
        pen.rotation_euler[0] = math.radians(5 + i * 3)
        pens.append(pen)

    return [holder] + pens


def create_notebook():
    """Create an open notebook."""
    nb_x = -0.2
    nb_y = 0.2

    # Notebook cover
    bpy.ops.mesh.primitive_cube_add(
        size=1, location=(nb_x, nb_y, DESK["height"] + 0.015)
    )
    cover = bpy.context.active_object
    cover.name = clean_name("Props", "Notebook_Cover")
    cover.scale = (0.2, 0.15, 0.01)
    bpy.ops.object.transform_apply(scale=True)

    # Pages (slightly offset for thickness)
    bpy.ops.mesh.primitive_cube_add(
        size=1, location=(nb_x, nb_y, DESK["height"] + 0.01)
    )
    pages = bpy.context.active_object
    pages.name = clean_name("Props", "Notebook_Pages")
    pages.scale = (0.19, 0.14, 0.008)
    bpy.ops.object.transform_apply(scale=True)

    # Spine
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.005, depth=0.15, location=(nb_x - 0.1, nb_y, DESK["height"] + 0.015)
    )
    spine = bpy.context.active_object
    spine.name = clean_name("Props", "Notebook_Spine")
    spine.rotation_euler[0] = math.radians(90)

    return [cover, pages, spine]


def create_desk_lamp():
    """Create articulated desk lamp."""
    lamp_x = DESK["width"] / 2 - 0.2
    lamp_y = -0.2

    # Base
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.06, depth=0.02, location=(lamp_x, lamp_y, DESK["height"] + 0.01)
    )
    base = bpy.context.active_object
    base.name = clean_name("Props", "LampBase")

    # Lower arm
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.01, depth=0.3, location=(lamp_x, lamp_y, DESK["height"] + 0.17)
    )
    arm_lower = bpy.context.active_object
    arm_lower.name = clean_name("Props", "LampArm_Lower")
    arm_lower.rotation_euler[0] = math.radians(-15)

    # Upper arm
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.008,
        depth=0.25,
        location=(lamp_x - 0.05, lamp_y, DESK["height"] + 0.35),
    )
    arm_upper = bpy.context.active_object
    arm_upper.name = clean_name("Props", "LampArm_Upper")
    arm_upper.rotation_euler[0] = math.radians(20)

    # Shade
    bpy.ops.mesh.primitive_cone_add(
        radius1=0.06,
        radius2=0.03,
        depth=0.08,
        location=(lamp_x - 0.08, lamp_y, DESK["height"] + 0.45),
    )
    shade = bpy.context.active_object
    shade.name = clean_name("Props", "LampShade")

    # Bulb (emissive)
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.02, location=(lamp_x - 0.08, lamp_y, DESK["height"] + 0.42)
    )
    bulb = bpy.context.active_object
    bulb.name = clean_name("Props", "LampBulb")

    return [base, arm_lower, arm_upper, shade, bulb]


# ============================================================
# CABLE MANAGEMENT
# ============================================================


def create_cable_management():
    """Create cable management under desk."""
    cables = []

    # Cable tray
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.2, DESK["height"] - 0.1))
    tray = bpy.context.active_object
    tray.name = clean_name("Cable", "Tray")
    tray.scale = (1.0, 0.08, 0.03)
    bpy.ops.object.transform_apply(scale=True)

    cables.append(tray)

    # Cable bundle (decorative)
    for i in range(3):
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.008,
            depth=0.5,
            location=(0.1 * i - 0.1, -0.3, DESK["height"] - 0.05),
        )
        cable = bpy.context.active_object
        cable.name = clean_name("Cable", f"Bundle_{i}")
        cable.rotation_euler[0] = math.radians(70 + i * 10)
        cables.append(cable)

    return cables


# ============================================================
# MATERIALS
# ============================================================


def get_materials():
    """Get or create all desk materials."""
    materials = {
        "MAT_Aged_Walnut": create_material(
            "MAT_Aged_Walnut", (0.24, 0.17, 0.12), roughness=0.75, metallic=0.0
        ),
        "MAT_Brushed_Metal": create_material(
            "MAT_Brushed_Metal", (0.54, 0.54, 0.54), roughness=0.50, metallic=0.85
        ),
        "MAT_Paper": create_material(
            "MAT_Paper", (0.96, 0.95, 0.93), roughness=0.90, metallic=0.0
        ),
        "MAT_Ceramic": create_material(
            "MAT_Ceramic", (0.9, 0.9, 0.9), roughness=0.30, metallic=0.0
        ),
        "MAT_Coffee": create_material(
            "MAT_Coffee", (0.15, 0.08, 0.04), roughness=0.20, metallic=0.0
        ),
        "MAT_Leather": create_material(
            "MAT_Leather", (0.16, 0.12, 0.08), roughness=0.60, metallic=0.0
        ),
        "MAT_Warm_Light": create_material(
            "MAT_Warm_Light", (1.0, 0.8, 0.6), roughness=0.10, metallic=0.0
        ),
        "MAT_Black_Plastic": create_material(
            "MAT_Black_Plastic", (0.05, 0.05, 0.05), roughness=0.40, metallic=0.0
        ),
    }

    # Add emission to warm light
    warm = materials["MAT_Warm_Light"]
    warm.node_tree.nodes["Principled BSDF"].inputs["Emission Color"].default_value = (
        1.0,
        0.8,
        0.6,
        1,
    )
    warm.node_tree.nodes["Principled BSDF"].inputs[
        "Emission Strength"
    ].default_value = 2.0

    return materials


def apply_materials(objects, materials):
    """Apply materials to objects."""
    material_map = {
        "Surface": "MAT_Aged_Walnut",
        "Housing": "MAT_Aged_Walnut",
        "Drawer": "MAT_Aged_Walnut",
        "Handle": "MAT_Brushed_Metal",
        "Leg": "MAT_Brushed_Metal",
        "Foot": "MAT_Black_Plastic",
        "Main": "MAT_Aged_Walnut",
        "Shelf": "MAT_Aged_Walnut",
        "Bracket": "MAT_Brushed_Metal",
        "Clamp": "MAT_Brushed_Metal",
        "Pole": "MAT_Brushed_Metal",
        "Arm": "MAT_Brushed_Metal",
        "VESA": "MAT_Brushed_Metal",
        "CoffeeCup": "MAT_Ceramic",
        "CupHandle": "MAT_Ceramic",
        "Coffee": "MAT_Coffee",
        "PenHolder": "MAT_Ceramic",
        "Pen": "MAT_Black_Plastic",
        "Notebook_Cover": "MAT_Leather",
        "Notebook_Pages": "MAT_Paper",
        "Notebook_Spine": "MAT_Brushed_Metal",
        "LampBase": "MAT_Brushed_Metal",
        "LampArm": "MAT_Brushed_Metal",
        "LampShade": "MAT_Black_Plastic",
        "LampBulb": "MAT_Warm_Light",
        "Tray": "MAT_Brushed_Metal",
        "Bundle": "MAT_Black_Plastic",
    }

    for obj in objects:
        for key, mat_name in material_map.items():
            if key in obj.name:
                if mat_name in materials:
                    obj.data.materials.append(materials[mat_name])
                break


# ============================================================
# COLLECTION
# ============================================================


def setup_collection():
    """Create and setup collection for desk."""
    col_name = "Central_Core_Desk"

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
    print("MVXWorld — Creation Desk Build")
    print("=" * 50)

    # Setup collection
    col = setup_collection()

    # Get materials
    materials = get_materials()

    all_objects = []

    # Create desk surface
    print("\n[1/8] Creating desk surface...")
    surface = create_desk_surface()
    all_objects.append(surface)

    # Create drawer units
    print("[2/8] Creating drawer units...")
    housing_l, drawers_l = create_drawer_unit("left")
    housing_r, drawers_r = create_drawer_unit("right")
    all_objects.extend([housing_l, housing_r])
    all_objects.extend(drawers_l)
    all_objects.extend(drawers_r)

    # Create legs
    print("[3/8] Creating desk legs...")
    legs = create_legs()
    all_objects.extend(legs)

    # Create back panel
    print("[4/8] Creating back panel...")
    panel, shelves = create_back_panel()
    all_objects.append(panel)
    all_objects.extend(shelves)

    # Create monitor arm
    print("[5/8] Creating monitor arm...")
    monitor_parts = create_monitor_arm()
    all_objects.extend(monitor_parts)

    # Create props
    print("[6/8] Creating desk props...")
    coffee = create_coffee_cup()
    pens = create_pen_holder()
    notebook = create_notebook()
    lamp = create_desk_lamp()
    all_objects.extend(coffee)
    all_objects.extend(pens)
    all_objects.extend(notebook)
    all_objects.extend(lamp)

    # Create cable management
    print("[7/8] Creating cable management...")
    cables = create_cable_management()
    all_objects.extend(cables)

    # Apply materials
    print("[8/8] Applying materials...")
    apply_materials(all_objects, materials)

    # Link to collection
    for obj in all_objects:
        link_to_collection(obj, col)

    # Deselect all
    bpy.ops.object.select_all(action="DESELECT")

    print("\n" + "=" * 50)
    print("CREATION DESK COMPLETE")
    print("=" * 50)
    print(f"\nTotal objects: {len(all_objects)}")
    print("\nComponents:")
    print("  - Desk surface (aged walnut)")
    print("  - Drawer units (left + right)")
    print("  - Desk legs (brushed metal)")
    print("  - Back panel with shelves")
    print("  - Monitor arm mount")
    print("  - Coffee cup")
    print("  - Pen holder + pens")
    print("  - Notebook")
    print("  - Articulated desk lamp")
    print("  - Cable management")
    print("\nNext steps:")
    print("1. Add subdivision for smooth surfaces")
    print("2. Unwrap UVs for texturing")
    print("3. Add surface imperfections")
    print("4. Place in Central Core zone")


if __name__ == "__main__":
    main()
