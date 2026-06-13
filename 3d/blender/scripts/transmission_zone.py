"""
MVXWorld — Transmission Zone (Signal Corner)
Run in Blender 4.0+ after graybox is loaded.

Usage:
1. Open MVXWorld_Room.blend
2. Switch to Scripting workspace
3. Open this file or paste contents
4. Click "Run Script"

Generates:
- Holographic projection rig
- Signal receiver device
- Data stream particles
- Frequency display
- Waveform visualization
- Transmission artifacts
"""

import bpy
import math
from mathutils import Vector, noise

# ============================================================
# CONFIGURATION
# ============================================================

ZONE = {
    "center": (3.5, -3.0, 0),
    "size": (2.5, 2.5),
}

RIG = {
    "base_size": (0.4, 0.4, 0.05),
    "pole_height": 1.8,
    "pole_radius": 0.025,
    "ring_radius": 0.35,
    "ring_thickness": 0.03,
    "ring_count": 3,
}

RECEIVER = {
    "body_size": (0.3, 0.2, 0.5),
    "antenna_height": 0.4,
    "screen_size": (0.2, 0.15),
}

DISPLAY = {
    "width": 0.4,
    "height": 0.25,
    "depth": 0.02,
    "stand_height": 0.3,
}

STREAM = {
    "particle_count": 200,
    "stream_width": 0.15,
    "stream_height": 1.5,
    "speed": 0.5,
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


def add_bevel(obj, width=0.003, segments=2):
    """Add bevel modifier."""
    bevel = obj.modifiers.new(name="Bevel", type="BEVEL")
    bevel.width = width
    bevel.segments = segments
    bevel.limit_method = "ANGLE"
    bevel.angle_limit = math.radians(30)
    return bevel


# ============================================================
# HOLOGRAPHIC RIG
# ============================================================


def create_holographic_rig():
    """Create the main holographic projection system."""
    x, y, z = ZONE["center"]
    parts = []

    # Base platform
    bpy.ops.mesh.primitive_cylinder_add(
        radius=RIG["base_size"][0] / 2,
        depth=RIG["base_size"][2],
        location=(x, y, z + RIG["base_size"][2] / 2),
    )
    base = bpy.context.active_object
    base.name = clean_name("Rig", "Base")
    parts.append(base)

    # Center pole
    bpy.ops.mesh.primitive_cylinder_add(
        radius=RIG["pole_radius"],
        depth=RIG["pole_height"],
        location=(x, y, z + RIG["pole_height"] / 2 + RIG["base_size"][2]),
    )
    pole = bpy.context.active_object
    pole.name = clean_name("Rig", "Pole")
    parts.append(pole)

    # Projection rings
    for i in range(RIG["ring_count"]):
        ring_z = z + 0.8 + i * 0.4
        ring_radius = RIG["ring_radius"] - i * 0.05

        bpy.ops.mesh.primitive_torus_add(
            major_radius=ring_radius,
            minor_radius=RIG["ring_thickness"],
            location=(x, y, ring_z),
        )
        ring = bpy.context.active_object
        ring.name = clean_name("Rig", f"Ring_{i}")

        # Tilt rings slightly
        ring.rotation_euler[0] = math.radians(15 + i * 10)
        ring.rotation_euler[2] = math.radians(i * 30)

        parts.append(ring)

    # Central emitter (sphere)
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.08, location=(x, y, z + RIG["pole_height"] + RIG["base_size"][2])
    )
    emitter = bpy.context.active_object
    emitter.name = clean_name("Rig", "Emitter")
    parts.append(emitter)

    return parts


# ============================================================
# SIGNAL RECEIVER
# ============================================================


def create_signal_receiver():
    """Create signal receiver device."""
    x, y, z = ZONE["center"]
    offset_x = 0.8
    offset_y = -0.5
    parts = []

    # Receiver body
    bpy.ops.mesh.primitive_cube_add(
        size=1, location=(x + offset_x, y + offset_y, z + RECEIVER["body_size"][2] / 2)
    )
    body = bpy.context.active_object
    body.name = clean_name("Receiver", "Body")
    body.scale = RECEIVER["body_size"]
    bpy.ops.object.transform_apply(scale=True)
    add_bevel(body, width=0.005)
    parts.append(body)

    # Screen
    bpy.ops.mesh.primitive_plane_add(
        size=1,
        location=(
            x + offset_x,
            y + offset_y - RECEIVER["body_size"][1] / 2 - 0.005,
            z + RECEIVER["body_size"][2] * 0.6,
        ),
    )
    screen = bpy.context.active_object
    screen.name = clean_name("Receiver", "Screen")
    screen.scale = (RECEIVER["screen_size"][0], RECEIVER["screen_size"][1], 1)
    screen.rotation_euler[0] = math.radians(90)
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    parts.append(screen)

    # Antenna
    bpy.ops.mesh.primitive_cone_add(
        radius1=0.015,
        radius2=0.003,
        depth=RECEIVER["antenna_height"],
        location=(
            x + offset_x + 0.1,
            y + offset_y,
            z + RECEIVER["body_size"][2] + RECEIVER["antenna_height"] / 2,
        ),
    )
    antenna = bpy.context.active_object
    antenna.name = clean_name("Receiver", "Antenna")
    parts.append(antenna)

    # Antenna tip (glowing)
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.01,
        location=(
            x + offset_x + 0.1,
            y + offset_y,
            z + RECEIVER["body_size"][2] + RECEIVER["antenna_height"],
        ),
    )
    tip = bpy.context.active_object
    tip.name = clean_name("Receiver", "AntennaTip")
    parts.append(tip)

    # Knobs
    for i in range(3):
        knob_x = x + offset_x - 0.08 + i * 0.08

        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.012,
            depth=0.015,
            location=(
                knob_x,
                y + offset_y - RECEIVER["body_size"][1] / 2 - 0.01,
                z + 0.1,
            ),
        )
        knob = bpy.context.active_object
        knob.name = clean_name("Receiver", f"Knob_{i}")
        knob.rotation_euler[0] = math.radians(90)
        parts.append(knob)

    return parts


# ============================================================
# FREQUENCY DISPLAY
# ============================================================


def create_frequency_display():
    """Create frequency readout display."""
    x, y, z = ZONE["center"]
    offset_x = -0.6
    parts = []

    # Display housing
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(
            x + offset_x,
            y + 0.3,
            z + DISPLAY["stand_height"] + DISPLAY["height"] / 2,
        ),
    )
    housing = bpy.context.active_object
    housing.name = clean_name("Display", "Housing")
    housing.scale = (DISPLAY["width"], DISPLAY["depth"], DISPLAY["height"])
    bpy.ops.object.transform_apply(scale=True)
    add_bevel(housing, width=0.003)
    parts.append(housing)

    # Screen surface
    bpy.ops.mesh.primitive_plane_add(
        size=1,
        location=(
            x + offset_x,
            y + 0.3 - DISPLAY["depth"] / 2 - 0.003,
            z + DISPLAY["stand_height"] + DISPLAY["height"] / 2,
        ),
    )
    screen = bpy.context.active_object
    screen.name = clean_name("Display", "Screen")
    screen.scale = (DISPLAY["width"] * 0.9, DISPLAY["height"] * 0.9, 1)
    screen.rotation_euler[0] = math.radians(90)
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    parts.append(screen)

    # Stand
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.02,
        depth=DISPLAY["stand_height"],
        location=(x + offset_x, y + 0.3, z + DISPLAY["stand_height"] / 2),
    )
    stand = bpy.context.active_object
    stand.name = clean_name("Display", "Stand")
    parts.append(stand)

    # Stand base
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.06, depth=0.01, location=(x + offset_x, y + 0.3, z + 0.005)
    )
    stand_base = bpy.context.active_object
    stand_base.name = clean_name("Display", "StandBase")
    parts.append(stand_base)

    return parts


# ============================================================
# WAVEFORM VISUALIZATION
# ============================================================


def create_waveform():
    """Create 3D waveform visualization."""
    x, y, z = ZONE["center"]
    parts = []

    # Create curve for waveform
    curve_data = bpy.data.curves.new("WaveformCurve", type="CURVE")
    curve_data.dimensions = "3D"
    curve_data.bevel_depth = 0.008
    curve_data.bevel_resolution = 4

    spline = curve_data.splines.new("NURBS")
    spline.points.add(49)  # 50 points total

    for i in range(50):
        t = i / 49.0
        wave_x = x - 0.5 + t * 1.0
        wave_y = y - 0.8
        wave_z = z + 0.5 + math.sin(t * math.pi * 4) * 0.15 + noise.random() * 0.02

        spline.points[i].co = (wave_x, wave_y, wave_z, 1)

    spline.use_endpoint_u = True
    spline.order_u = 4

    waveform_obj = bpy.data.objects.new("Waveform", curve_data)
    bpy.context.collection.objects.link(waveform_obj)
    waveform_obj.name = clean_name("FX", "Waveform")
    parts.append(waveform_obj)

    return parts


# ============================================================
# DATA STREAMS (Particle System)
# ============================================================


def create_data_streams():
    """Create data stream particle emitters."""
    x, y, z = ZONE["center"]
    parts = []

    # Create emitter planes
    for i in range(3):
        stream_x = x - 0.3 + i * 0.3
        stream_y = y - 0.2

        bpy.ops.mesh.primitive_plane_add(
            size=STREAM["stream_width"], location=(stream_x, stream_y, z + 0.2)
        )
        emitter = bpy.context.active_object
        emitter.name = clean_name("DataStream", f"Emitter_{i}")
        emitter.rotation_euler[0] = math.radians(90)
        bpy.ops.object.transform_apply(scale=True, rotation=True)

        # Add particle system
        bpy.ops.object.particle_system_add()
        ps = emitter.particle_systems[0]
        ps.name = f"DataStream_{i}"

        # Configure particles
        settings = ps.settings
        settings.count = STREAM["particle_count"]
        settings.lifetime = 2.0
        settings.frame_start = 1
        settings.frame_end = 250
        settings.emit_from = "FACE"
        settings.physics_type = "NEWTON"
        settings.normal_factor = STREAM["speed"]
        settings.factor_random = 0.1

        # Render settings
        settings.render_type = "HALO"
        settings.particle_size = 0.005
        settings.size_random = 0.5

        parts.append(emitter)

    return parts


# ============================================================
# TRANSMISSION ARTIFACTS
# ============================================================


def create_artifacts():
    """Create mysterious transmission artifacts."""
    x, y, z = ZONE["center"]
    parts = []

    # Floating message tablets
    tablet_positions = [
        (x + 0.5, y + 0.3, z + 1.2),
        (x - 0.4, y + 0.5, z + 0.9),
        (x + 0.2, y - 0.3, z + 1.5),
    ]

    for i, pos in enumerate(tablet_positions):
        bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
        tablet = bpy.context.active_object
        tablet.name = clean_name("Artifact", f"Tablet_{i}")
        tablet.scale = (0.15, 0.01, 0.2)
        tablet.rotation_euler[1] = math.radians(noise.random() * 20 - 10)
        tablet.rotation_euler[2] = math.radians(noise.random() * 30 - 15)
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        add_bevel(tablet, width=0.002)
        parts.append(tablet)

    # Signal orbs
    for i in range(5):
        angle = i * 72
        orb_x = x + math.cos(math.radians(angle)) * 0.6
        orb_y = y + math.sin(math.radians(angle)) * 0.6
        orb_z = z + 0.8 + noise.random() * 0.5

        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.02 + noise.random() * 0.02, location=(orb_x, orb_y, orb_z)
        )
        orb = bpy.context.active_object
        orb.name = clean_name("Artifact", f"Orb_{i}")
        parts.append(orb)

    return parts


# ============================================================
# LIGHTING
# ============================================================


def create_lighting():
    """Create transmission zone lighting."""
    x, y, z = ZONE["center"]
    parts = []

    # Main holographic light (acid green)
    bpy.ops.object.light_add(type="POINT", location=(x, y, z + 2.0))
    holo_light = bpy.context.active_object
    holo_light.name = clean_name("Light", "Holographic")
    holo_light.data.energy = 1000
    holo_light.data.color = (0.78, 1.0, 0.0)  # Acid green
    holo_light.data.shadow_soft_size = 0.5
    parts.append(holo_light)

    # Spot for receiver
    bpy.ops.object.light_add(type="SPOT", location=(x + 0.8, y - 0.5, z + 1.5))
    spot = bpy.context.active_object
    spot.name = clean_name("Light", "ReceiverSpot")
    spot.data.energy = 300
    spot.data.color = (0.8, 0.9, 1.0)  # Cool white
    spot.data.spot_size = math.radians(45)
    spot.rotation_euler[0] = math.radians(-60)
    parts.append(spot)

    return parts


# ============================================================
# MATERIALS
# ============================================================


def get_materials():
    """Get or create all materials."""
    materials = {
        "MAT_Dark_Metal": create_material(
            "MAT_Dark_Metal", (0.12, 0.12, 0.11), roughness=0.40, metallic=0.90
        ),
        "MAT_Brass_Tarnished": create_material(
            "MAT_Brass_Tarnished", (0.55, 0.48, 0.22), roughness=0.45, metallic=0.85
        ),
        "MAT_Screen_Dark": create_material(
            "MAT_Screen_Dark",
            (0.02, 0.02, 0.02),
            roughness=0.10,
            metallic=0.0,
            emission=(0.1, 0.15, 0.1),
            emission_strength=1.0,
        ),
        "MAT_Acid_Glow": create_material(
            "MAT_Acid_Glow",
            (0.78, 1.0, 0.0),
            roughness=0.20,
            metallic=0.70,
            emission=(0.78, 1.0, 0.0),
            emission_strength=5.0,
        ),
        "MAT_Holographic": create_material(
            "MAT_Holographic",
            (0.5, 0.8, 1.0),
            roughness=0.10,
            metallic=0.80,
            emission=(0.5, 0.8, 1.0),
            emission_strength=3.0,
        ),
        "MAT_Tablet_Stone": create_material(
            "MAT_Tablet_Stone", (0.25, 0.24, 0.22), roughness=0.70, metallic=0.0
        ),
        "MAT_Signal_Orb": create_material(
            "MAT_Signal_Orb",
            (0.9, 0.95, 1.0),
            roughness=0.10,
            metallic=0.0,
            emission=(0.9, 0.95, 1.0),
            emission_strength=4.0,
        ),
    }

    return materials


def apply_materials(objects, materials):
    """Apply materials to objects."""
    material_map = {
        "Base": "MAT_Dark_Metal",
        "Pole": "MAT_Brass_Tarnished",
        "Ring": "MAT_Acid_Glow",
        "Emitter": "MAT_Holographic",
        "Body": "MAT_Dark_Metal",
        "Screen": "MAT_Screen_Dark",
        "Antenna": "MAT_Brass_Tarnished",
        "AntennaTip": "MAT_Acid_Glow",
        "Knob": "MAT_Dark_Metal",
        "Housing": "MAT_Dark_Metal",
        "Stand": "MAT_Dark_Metal",
        "StandBase": "MAT_Dark_Metal",
        "Tablet": "MAT_Tablet_Stone",
        "Orb": "MAT_Signal_Orb",
    }

    for obj in objects:
        if not hasattr(obj, "name"):
            continue

        for key, mat_name in material_map.items():
            if key in obj.name:
                if mat_name in materials:
                    if obj.data and hasattr(obj.data, "materials"):
                        obj.data.materials.append(materials[mat_name])
                break


# ============================================================
# COLLECTION
# ============================================================


def setup_collection():
    """Create and setup collection."""
    col_name = "Transmission_Zone"

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
    print("MVXWorld — Transmission Zone")
    print("=" * 50)

    # Setup collection
    col = setup_collection()

    # Get materials
    materials = get_materials()

    all_objects = []

    # Create holographic rig
    print("\n[1/6] Creating holographic rig...")
    rig_parts = create_holographic_rig()
    all_objects.extend(rig_parts)

    # Create signal receiver
    print("[2/6] Creating signal receiver...")
    receiver_parts = create_signal_receiver()
    all_objects.extend(receiver_parts)

    # Create frequency display
    print("[3/6] Creating frequency display...")
    display_parts = create_frequency_display()
    all_objects.extend(display_parts)

    # Create waveform
    print("[4/6] Creating waveform visualization...")
    waveform_parts = create_waveform()
    all_objects.extend(waveform_parts)

    # Create data streams
    print("[5/6] Creating data streams...")
    stream_parts = create_data_streams()
    all_objects.extend(stream_parts)

    # Create artifacts
    print("[6/6] Creating transmission artifacts...")
    artifact_parts = create_artifacts()
    all_objects.extend(artifact_parts)

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
    print("TRANSMISSION ZONE COMPLETE")
    print("=" * 50)
    print(f"\nTotal objects: {len(all_objects)}")
    print("\nComponents:")
    print("  - Holographic projection rig")
    print("  - Signal receiver device")
    print("  - Frequency display")
    print("  - Waveform visualization")
    print("  - Data stream emitters (3)")
    print("  - Transmission tablets (3)")
    print("  - Signal orbs (5)")
    print("  - Zone lighting")
    print("\nMaterials applied:")
    print("  - Acid green emission (rings)")
    print("  - Holographic blue (emitter)")
    print("  - Dark metal (structure)")
    print("  - Tarnished brass (accents)")
    print("\nNext steps:")
    print("1. Configure particle systems")
    print("2. Add animation to rings")
    print("3. Create screen textures")
    print("4. Test emission values")


if __name__ == "__main__":
    main()
