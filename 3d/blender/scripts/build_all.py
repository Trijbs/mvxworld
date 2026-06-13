"""
MVXWorld — Master Build Script
Run in Blender 4.0+ to build the complete scene.

Usage:
1. Open Blender (default scene)
2. Switch to Scripting workspace
3. Open this file or paste contents
4. Click "Run Script"

This script runs all zone scripts in sequence:
1. Graybox blockout
2. Creation Desk (Central Core)
3. Memory Wall
4. Transmission Zone
5. Archive Shelves
6. Discovery Zone
7. Final lighting and camera setup

Total build time: ~2-5 minutes depending on hardware.
"""

import bpy
import sys
import os
from pathlib import Path

# ============================================================
# CONFIGURATION
# ============================================================

SCRIPTS_DIR = Path(__file__).parent

SCRIPTS = [
    ("graybox_blockout.py", "Graybox Blockout"),
    ("creation_desk.py", "Creation Desk"),
    ("memory_wall.py", "Memory Wall"),
    ("transmission_zone.py", "Transmission Zone"),
    ("archive_shelves.py", "Archive Shelves"),
    ("discovery_zone.py", "Discovery Zone"),
]

# ============================================================
# UTILITIES
# ============================================================


def clean_scene():
    """Remove all objects from scene."""
    print("\n[CLEAN] Removing default objects...")

    # Select all
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    # Remove default collections
    for col in bpy.data.collections:
        if col.name != "Collection":
            bpy.data.collections.remove(col)

    # Remove default lights, cameras, meshes
    for obj in bpy.data.objects:
        bpy.data.objects.remove(obj)

    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)

    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat)

    for light in bpy.data.lights:
        bpy.data.lights.remove(light)

    for cam in bpy.data.cameras:
        bpy.data.cameras.remove(cam)

    print("[CLEAN] Scene cleared.")


def run_script(script_path, script_name):
    """Execute a Blender Python script."""
    print(f"\n{'=' * 50}")
    print(f"[BUILD] {script_name}")
    print(f"{'=' * 50}")

    if not script_path.exists():
        print(f"[ERROR] Script not found: {script_path}")
        return False

    try:
        # Read script content
        with open(script_path, "r") as f:
            script_content = f.read()

        # Execute in Blender's namespace
        exec(
            compile(script_content, str(script_path), "exec"),
            {
                "__builtins__": __builtins__,
                "__name__": "__main__",
                "__file__": str(script_path),
            },
        )

        print(f"[OK] {script_name} completed successfully.")
        return True

    except Exception as e:
        print(f"[ERROR] {script_name} failed: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


def setup_final_lighting():
    """Setup final scene lighting."""
    print("\n[LIGHTS] Setting up final lighting...")

    # Ensure we're in object mode
    if bpy.context.object and bpy.context.object.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")

    # Volumetric fog
    world = bpy.context.scene.world
    if not world:
        world = bpy.data.worlds.new("MVXWorld_World")
        bpy.context.scene.world = world

    world.use_nodes = True
    nodes = world.node_tree.nodes
    links = world.node_tree.links

    # Clear existing nodes
    for node in nodes:
        nodes.remove(node)

    # Create world shader
    output = nodes.new("ShaderNodeOutputWorld")
    output.location = (400, 0)

    background = nodes.new("ShaderNodeBackground")
    background.location = (200, 0)
    background.inputs["Color"].default_value = (0.01, 0.01, 0.01, 1)
    background.inputs["Strength"].default_value = 0.3

    # Volume scatter for atmosphere
    volume = nodes.new("ShaderNodeVolumeScatter")
    volume.location = (200, -200)
    volume.inputs["Color"].default_value = (0.9, 0.9, 0.85, 1)
    volume.inputs["Density"].default_value = 0.02
    volume.inputs["Anisotropy"].default_value = 0.3

    # Connect
    links.new(background.outputs["Background"], output.inputs["Surface"])
    links.new(volume.outputs["Volume"], output.inputs["Volume"])

    print("[LIGHTS] Volumetric atmosphere added.")


def setup_final_cameras():
    """Setup final camera system."""
    print("\n[CAMERAS] Setting up camera system...")

    # Ensure we're in object mode
    if bpy.context.object and bpy.context.object.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")

    # Check if any cameras exist
    cameras = [obj for obj in bpy.data.objects if obj.type == "CAMERA"]

    if not cameras:
        print("[CAMERAS] No cameras found, creating default...")

        bpy.ops.object.camera_add(location=(0, 8.0, 1.65))
        cam = bpy.context.active_object
        cam.name = "CAM_Default"
        cam.data.lens = 35

        # Point at scene center
        direction = cam.location.copy()
        direction.y = 0
        direction.z = 1.5
        cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()

    # Set first camera as active
    bpy.context.scene.camera = cameras[0] if cameras else bpy.context.active_object

    print(f"[CAMERAS] {len(cameras)} cameras configured.")


def setup_render_settings():
    """Configure render settings."""
    print("\n[RENDER] Configuring render settings...")

    scene = bpy.context.scene

    # Resolution
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100

    # Engine (Eevee for speed)
    scene.render.engine = "BLENDER_EEVEE"

    # Eevee settings (handle Blender 4.0+ API changes)
    eevee = scene.eevee

    # Blender 4.0+ uses Eevee Next with different settings
    # Use try/except for backward compatibility
    try:
        # Blender 4.0+ Eevee Next
        if hasattr(eevee, "use_shadows"):
            eevee.use_shadows = True
        if hasattr(eevee, "shadow_pool_size"):
            eevee.shadow_pool_size = 1024
        if hasattr(eevee, "use_volumetric_shadows"):
            eevee.use_volumetric_shadows = True
        if hasattr(eevee, "volumetric_shadow_samples"):
            eevee.volumetric_shadow_samples = 64
        # Bloom may be removed in 4.0+, use compositor instead
        if hasattr(eevee, "use_bloom"):
            eevee.use_bloom = True
            eevee.bloom_intensity = 0.05
        # SSR settings
        if hasattr(eevee, "use_ssr"):
            eevee.use_ssr = True
        if hasattr(eevee, "use_ssr_refraction"):
            eevee.use_ssr_refraction = True
        # AO settings
        if hasattr(eevee, "use_gtao"):
            eevee.use_gtao = True
            eevee.gtao_distance = 0.5
        elif hasattr(eevee, "use_ambient_occlusion"):
            eevee.use_ambient_occlusion = True
        print("[RENDER] Eevee settings configured.")
    except Exception as e:
        print(
            f"[RENDER] Some Eevee settings skipped (Blender version compatibility): {e}"
        )

    # Output
    scene.render.filepath = "//renders/"
    scene.render.image_settings.file_format = "PNG"

    # Performance
    scene.render.threads_mode = "AUTO"

    print("[RENDER] Settings configured for Eevee.")


def print_scene_stats():
    """Print scene statistics."""
    print("\n" + "=" * 50)
    print("SCENE STATISTICS")
    print("=" * 50)

    # Objects by type
    mesh_count = len([obj for obj in bpy.data.objects if obj.type == "MESH"])
    light_count = len([obj for obj in bpy.data.objects if obj.type == "LIGHT"])
    camera_count = len([obj for obj in bpy.data.objects if obj.type == "CAMERA"])
    curve_count = len([obj for obj in bpy.data.objects if obj.type == "CURVE"])

    print(f"\nObjects:")
    print(f"  Meshes: {mesh_count}")
    print(f"  Lights: {light_count}")
    print(f"  Cameras: {camera_count}")
    print(f"  Curves: {curve_count}")
    print(f"  Total: {mesh_count + light_count + camera_count + curve_count}")

    # Collections
    print(f"\nCollections: {len(bpy.data.collections)}")
    for col in bpy.data.collections:
        obj_count = len(col.objects)
        print(f"  - {col.name}: {obj_count} objects")

    # Materials
    print(f"\nMaterials: {len(bpy.data.materials)}")

    # Polycount (estimate)
    total_polys = 0
    for obj in bpy.data.objects:
        if obj.type == "MESH" and obj.data:
            total_polys += len(obj.data.polygons)

    print(f"\nPolygons: {total_polys:,}")
    print(f"Est. Triangles: {total_polys * 2:,}")


# ============================================================
# MAIN EXECUTION
# ============================================================


def main():
    """Main execution function."""
    print("\n" + "=" * 60)
    print("MVXWORLD — MASTER BUILD")
    print("=" * 60)
    print("\nBuilding complete MVXWorld immersive room...")
    print("This may take 2-5 minutes.\n")

    # Clean scene
    clean_scene()

    # Run each script
    success_count = 0
    total_scripts = len(SCRIPTS)

    for script_file, script_name in SCRIPTS:
        script_path = SCRIPTS_DIR / script_file

        if run_script(script_path, script_name):
            success_count += 1
        else:
            print(f"\n[WARNING] {script_name} had errors, continuing...")

    # Final setup
    print("\n" + "=" * 60)
    print("FINAL CONFIGURATION")
    print("=" * 60)

    setup_final_lighting()
    setup_final_cameras()
    setup_render_settings()

    # Print stats
    print_scene_stats()

    # Summary
    print("\n" + "=" * 60)
    print("BUILD COMPLETE")
    print("=" * 60)
    print(f"\nScripts executed: {success_count}/{total_scripts}")

    if success_count == total_scripts:
        print("\n✓ All zones built successfully!")
    else:
        print(f"\n⚠ {total_scripts - success_count} script(s) had errors")

    print("\nNext steps:")
    print("1. Save as 'MVXWorld_Room.blend'")
    print("2. Review each zone (Collections panel)")
    print("3. Test camera shots (CAM_ objects)")
    print("4. Adjust lighting as needed")
    print("5. Add textures and UV unwrapping")
    print("6. Render preview (F12)")
    print("7. Export for Three.js (glTF 2.0)")

    print("\nFile location:")
    print(f"  {SCRIPTS_DIR.parent / 'scenes' / 'MVXWorld_Room.blend'}")

    # Deselect all
    bpy.ops.object.select_all(action="DESELECT")


if __name__ == "__main__":
    main()
