# MVXWORLD IMMERSIVE ROOM — PRODUCTION SPECIFICATION v2.0
## Enhanced Build Specification for Blender + Three.js/WebGL Pipeline

**Domain:** mvxworld.art  
**Subdomains:** `room.mvxworld.art` (3D experience) · `studio.mvxworld.art` (creation hub) · `archive.mvxworld.art` (memory vault)  
**Status:** Build-ready specification  
**Target:** Blender 4.x (Cycles/Eevee) → Three.js r160+ export

---

## ROLE

You are a Senior Environment TD, Blender Technical Artist, and Real-Time World Builder specializing in production-ready environments for Blender (Cycles/Eevee) and WebGL/Three.js export pipelines.

**Your task:** Transform the MVXWorld concept into a complete, production-ready 3D environment specification with strict real-world metrics, scene construction rules, asset breakdowns, material definitions, lighting values, camera design, and optimization strategy.

**Output requirement:** Directly usable by a 3D artist building the scene in Blender. This is NOT conceptual writing—this is a BUILD SPECIFICATION.

---

## 1. CORE WORLD IDENTITY

### 1.1 Concept
Design a fully immersive environment representing MVXWorld—a living creative universe where memory, imagination, experimentation, and unfinished ideas physically coexist.

### 1.2 Definition
> "A physical manifestation of a world-builder's mind in active creation."

### 1.3 Hard Constraints
| DO NOT | AVOID |
|--------|-------|
| Cyberpunk tropes | Neon overload, rain-slicked streets, holographic ads |
| Futuristic apartment | Sterile smart-home, voice assistants, floating UI |
| Sterile sci-fi | Clinical white, Apple-store minimalism |
| Tech showroom | Display-case perfection, corporate polish |

### 1.4 Required Character
| Quality | Expression |
|---------|------------|
| Handcrafted | Tool marks, visible construction, imperfect joins |
| Lived-in | Dust, wear patterns, moved-aside objects |
| Symbolic | Objects imply meaning without explanation |
| Evolving | Half-built things, open notebooks, active experiments |
| Human-scale | Everything reachable, usable, intimate |

---

## 2. BRAND INTEGRATION (Existing Design System)

### 2.1 Color Token Mapping
| Token | Hex | 3D Application |
|-------|-----|----------------|
| `--ink-base` | `#0a0a09` | Primary environment base, shadow color, void |
| `--ink-surface` | `#1a1a18` | Wall surfaces, furniture bodies, shelving |
| `--paper` | `#f5f3ee` | Light accents, text elements, paper props |
| `--paper-deep` | `#ebe7dc` | Warm light areas, parchment, aged surfaces |
| `--acid` | `#c8ff00` | **RESTRICTED** — data streams, signal markers, active elements |
| `--burn` | `#ff4d1c` | **RARE** — anomalous energy, critical warnings, 1-2 instances max |
| `--mute` | `#7a7870` | Metadata, inactive elements, secondary text |

### 2.2 Typography in 3D Space
| Element | Treatment |
|---------|-----------|
| Display text (manifesto fragments) | Cormorant Garamond italic — embossed, projected, or etched |
| Technical labels | IBM Plex Mono — screen displays, coordinates, system readouts |
| Handwritten notes | Custom texture — scanned handwriting, layered on paper |

### 2.3 Texture Language
- **Grain overlay:** SVG noise at 6% opacity, `mix-blend-mode: overlay` equivalent in post-processing
- **Material imperfection:** Every surface has micro-variation — no perfect planes
- **Edge wear:** Softened edges on all hard-surface models

---

## 3. SPATIAL LAYOUT (REAL-WORLD METRICS)

### 3.1 Global Dimensions
| Parameter | Value | Notes |
|-----------|-------|-------|
| Room width | 8.0m | Generous but not cavernous |
| Room depth | 10.0m | Allows depth parallax |
| Room height | 3.5m | Slightly elevated for grandeur |
| Wall thickness | 0.15m | Solid, substantial |
| Ceiling thickness | 0.20m | Exposed beam potential |
| Floor thickness | 0.10m | Layered material (wood + stone) |
| Primary door | 1.0m × 2.2m | Arched top, heavy wood |
| Windows (×3) | 1.5m × 2.5m | Floor-to-ceiling, mullioned |

### 3.2 Human Scale Reference
| Element | Height | Notes |
|---------|--------|-------|
| Eye line (standing) | 1.65m | Camera default |
| Eye line (seated) | 1.15m | Desk work position |
| Reach height | 2.1m | Maximum comfortable shelf |
| Desk surface | 0.75m | Standard workstation |
| Chair seat | 0.45m | Seated position |
| Door handle | 1.00m | Natural grip |

---

## 4. ZONE ARCHITECTURE

### Zone A: Central Creation Core
**Position:** Scene origin (0, 0, 0)  
**Footprint:** 3.0m × 4.0m  
**Height range:** 0.75m (desk) to 2.1m (shelf top)  
**Function:** ACTIVE WORLD BUILDING HUB

**Assets:**
- Large handcrafted desk (aged walnut, 1.8m × 0.9m)
- Multi-display setup (2-3 screens, mixed orientation)
- Open sketchbooks (3-4, layered)
- Scattered notes and diagrams
- Partially built prototype (physical model)
- Tool set (rulers, calipers, marking tools)
- Desk lamp (articulated, warm brass)
- Coffee cup (half-full, steam particle system)

**Sightline:** Faces Memory Archive Wall

### Zone B: Memory Archive Wall
**Position:** (0, 0, -5.0) — North wall  
**Footprint:** 8.0m × 0.5m (wall-mounted)  
**Height range:** 0.5m to 3.0m  
**Function:** MEMORY STORAGE + STORY FRAGMENTATION

**Assets:**
- Floating frames (12-16, varied sizes, embedded in wall depth)
- Concept sketches (3-4 visible, others partially obscured)
- Old photographs with subtle distortion shader
- Symbolic markings (etched, painted, projected)
- Encrypted annotations (IBM Plex Mono, tiny)
- Map fragments with coordinate overlays
- Layered paper collage (texture depth)

**Sightline:** Viewed from Central Core and Discovery Zone

### Zone C: Transmission Corner (MVX Signal Zone)
**Position:** (3.5, 0, -3.0) — Northeast corner  
**Footprint:** 2.5m × 2.5m  
**Height range:** 0.0m (floor) to 3.5m (ceiling projection)  
**Function:** EXTERNAL COMMUNICATION FROM MVXWORLD

**Assets:**
- Holographic projection system (custom rig)
- Floating fragmented text streams (particle-driven)
- Audio waveform visualization (3D mesh)
- Light particles reacting to unseen input
- Signal receiver device (physical object)
- Frequency display (IBM Plex Mono, real-time)
- Interdimensional message artifacts

**Key material:** `--acid` restricted to this zone (data streams only)

### Zone D: Archive Shelves
**Position:** (-3.5, 0, -2.0) — West wall  
**Footprint:** 3.0m × 0.6m  
**Height range:** 0.0m to 2.4m  
**Function:** KNOWLEDGE + MYSTERY STORAGE

**Assets:**
- Modular shelving (3 units, walnut + brushed metal)
- Books (20-30, varied sizes, some worn)
- Journals (5-8, leather-bound)
- Physical artifacts (8-12, ambiguous purpose)
- Miniature world models (3-4)
- Specimen jars (2-3, contents unclear)
- Shelf-integrated lighting (hidden LED strips)

**Sightline:** Profile view from Central Core

### Zone E: Discovery / Experiment Zone
**Position:** (0, 0, 3.0) — South area  
**Footprint:** 4.0m × 3.0m  
**Height range:** 0.5m (floor objects) to 2.8m (suspended)  
**Function:** CURIOUS EXPLORATION + UNKNOWN SYSTEMS

**Assets:**
- Floating geometric objects (5-8, varied materials)
- Half-finished mechanical inventions (2-3)
- Interactive abstract devices (3-4)
- Unknown physics-like mechanisms (2)
- Suspended experimental forms (ceiling-mounted)
- Workbench with active project
- Tool rack with specialized implements

**Key material:** `--burn` used sparingly here (anomalous energy)

---

## 5. ASSET PRODUCTION SPECIFICATIONS

### 5.1 Hero Assets

| Asset | Scale (m) | Polycount | Texture | UV Strategy | Material |
|-------|-----------|-----------|---------|-------------|----------|
| Creation Desk | 1.8×0.9×0.75 | 8K-12K | 2K atlas | Unique unwrap | Aged walnut |
| Display Array | 0.6×0.4×0.05 (×3) | 4K each | 1K each | Instance + unique | Brushed metal + glass |
| Archive Shelving | 1.0×0.4×2.4 (×3) | 6K each | 2K atlas | Modular tiling | Walnut + metal |
| Holographic Rig | 0.8×0.8×1.5 | 10K-15K | 2K unique | Unique unwrap | Brass + glass + emissive |
| Experiment Table | 1.5×0.8×0.75 | 5K-8K | 2K atlas | Unique unwrap | Worn wood + metal |

### 5.2 Medium Assets

| Asset | Scale (m) | Polycount | Texture | Notes |
|-------|-----------|-----------|---------|-------|
| Desk Chair | 0.5×0.5×0.9 | 4K-6K | 1K | Worn leather |
| Floating Frames | 0.3-0.8 (varied) | 1K each | 512 each | Instance with variation |
| Books | 0.2×0.03×0.3 | 500 each | 512 atlas | 20-30 instances |
| Journals | 0.25×0.04×0.35 | 600 each | 512 | 5-8 unique |
| Desk Lamp | 0.3×0.3×0.6 | 3K | 1K | Brass + glass |
| Signal Device | 0.4×0.4×0.8 | 5K | 1K | Mixed materials |

### 5.3 Small Props

| Asset | Scale (m) | Polycount | Texture | Notes |
|-------|-----------|-----------|---------|-------|
| Coffee Cup | 0.08×0.08×0.1 | 800 | 512 | Ceramic |
| Notes/Paper | 0.2×0.001×0.3 | 200 each | 1K atlas | 10-15 instances |
| Tools | 0.02-0.3 | 500-1K | 512 | 8-12 instances |
| Artifacts | 0.05-0.2 | 1K-2K | 512-1K | 8-12 unique |
| Geometric Objects | 0.1-0.5 | 2K-4K | 1K | 5-8 unique |
| Specimen Jars | 0.1×0.1×0.2 | 1.5K | 512 | Glass + contents |

---

## 6. PBR MATERIAL SYSTEM

### 6.1 Aged Walnut Wood
```
Base Color: #3d2b1f (dark) to #5c3a21 (light) — noise variation
Roughness: 0.65–0.80 (wear areas lower)
Metallic: 0.0
Specular: 0.40
Normal: Wood grain, strength 0.8
Imperfections: Scratches (normal), dust accumulation (roughness), edge wear (color lightening)
```

### 6.2 Brushed Metal (Non-chrome, Low Reflectivity)
```
Base Color: #8a8a8a with slight warmth
Roughness: 0.45–0.55 (directional brushing)
Metallic: 0.85
Specular: 0.50
Normal: Brushed pattern, strength 0.6
Imperfections: Fingerprints (roughness), minor scratches (normal)
```

### 6.3 Imperfect Glass
```
Base Color: #ffffff (clear) with slight blue tint
Roughness: 0.05–0.15 (varies by surface)
Metallic: 0.0
Specular: 0.95
Transmission: 0.90
IOR: 1.52
Imperfections: Slight distortion (normal), dust (roughness), edge chips
```

### 6.4 Paper (Layered, Slightly Warped)
```
Base Color: #f5f3ee to #ebe7dc — age variation
Roughness: 0.85–0.95
Metallic: 0.0
Specular: 0.20
Normal: Paper fiber texture, strength 0.4
Imperfections: Warping (displacement), ink bleed (color), yellowing edges
```

### 6.5 Worn Leather
```
Base Color: #2a1f14 (dark brown) with patina variation
Roughness: 0.55–0.70 (wear areas smoother)
Metallic: 0.0
Specular: 0.35
Normal: Leather grain + creases, strength 1.0
Imperfections: Cracking (normal), color fading (color), polish (roughness)
```

### 6.6 Emissive Holographic Surfaces
```
Base Color: #c8ff00 (acid green) — RESTRICTED USE
Emission Strength: 2.0–8.0 (varies by element)
Roughness: 0.10–0.30
Metallic: 0.70
Specular: 0.80
Animation: Subtle pulse (emission strength), data stream (UV scroll)
Notes: Only in Transmission Zone. Never dominant.
```

### 6.7 Stone (Floor Accent)
```
Base Color: #3a3a38 with mineral variation
Roughness: 0.75–0.90
Metallic: 0.0
Specular: 0.30
Normal: Stone texture, strength 1.2
Imperfections: Cracks (normal), moss (color), wear paths (roughness)
```

### 6.8 Brass (Fixtures, Hardware)
```
Base Color: #b5a642 with tarnish variation
Roughness: 0.35–0.50 (polished areas lower)
Metallic: 0.90
Specular: 0.60
Normal: Hammered/brushed, strength 0.5
Imperfections: Patina (color), fingerprints (roughness), verdigris (color)
```

---

## 7. LIGHTING DESIGN

### 7.1 Natural Light (Primary)

**Sun/Moon System:**
| Parameter | Value | Notes |
|-----------|-------|-------|
| Type | Sun (day) or Moon (night) | Scene supports both |
| Sun angle | 35° elevation, 220° azimuth | Late afternoon warmth |
| Sun intensity | 80,000–100,000 lux | Bright but not blown out |
| Moon intensity | 5,000–8,000 lux | Cool, mysterious |
| Color temp (day) | 5500K | Neutral warm |
| Color temp (night) | 8000K | Cool blue |

**Window Treatment:**
- Volumetric shafts through mullioned windows
- Floating dust particles visible in beams
- Soft falloff on floor (area light simulation)

### 7.2 Practical Lights

| Light | Type | Intensity | Color Temp | Position |
|-------|------|-----------|------------|----------|
| Desk Lamp | Spot | 800 lumens | 2700K (warm) | Creation Core |
| Shelf Strips | Area | 200 lumens/m | 3000K | Archive Shelves |
| Holographic Glow | Emission | Variable | 5600K + acid | Transmission Zone |
| Window Ambient | HDRI | 15,000 lux | 5500K | All windows |

### 7.3 Emissive Sources

| Element | Emission Strength | Color | Animation |
|---------|-------------------|-------|-----------|
| Data streams | 4.0–6.0 | `#c8ff00` | Scroll UV |
| Signal markers | 3.0–5.0 | `#c8ff00` | Pulse 0.5Hz |
| Warning elements | 2.0–3.0 | `#ff4d1c` | Flicker |
| Screen displays | 1.5–2.5 | `#f5f3ee` | Static |

### 7.4 Volumetric Settings

| Parameter | Value | Notes |
|-----------|-------|-------|
| Volume density | 0.02–0.05 | Light haze, not fog |
| Anisotropy | 0.3–0.5 | Forward scattering |
| Volume bounces | 2 | For realism |
| Shadow density | 0.8 | Substantial shadows |

### 7.5 Lighting Mood Map

| Zone | Primary | Secondary | Mood |
|------|---------|-----------|------|
| Creation Core | Desk lamp (warm) | Window light | Focused, intimate |
| Memory Wall | Shelf strips (cool) | Window spill | Archive, contemplative |
| Transmission | Emission (acid) | Desk lamp bleed | Mysterious, active |
| Archive Shelves | Strip lighting | Ambient | Knowledge, order |
| Discovery Zone | Mixed | Emission accents | Wonder, experimentation |

---

## 8. CAMERA SYSTEM

### 8.1 Default Viewport

| Parameter | Value |
|-----------|-------|
| Eye height (standing) | 1.65m |
| Eye height (seated) | 1.15m |
| Default lens | 35mm |
| Aperture | f/2.8–f/5.6 |
| Focus distance | 3.0–5.0m |

### 8.2 Lens Presets

| Lens | Use Case | DoF Setting |
|------|----------|-------------|
| 18mm | Establishing shot, spatial context | f/8–f/11 (deep) |
| 35mm | Standard exploration, balance | f/2.8–f/4.0 |
| 50mm | Intimate detail, portraits | f/1.8–f/2.8 |
| 85mm | Compressed detail, shallow focus | f/1.4–f/2.0 |

### 8.3 Cinematic Shot List

| Shot | Position (XYZ) | Look-at Target | Lens | Emotion |
|------|----------------|----------------|------|---------|
| 01 — The Arrival | (0, 1.65, 8.0) | (0, 1.2, 0) | 24mm | First impression, grandeur |
| 02 — The Desk | (1.5, 1.15, 1.5) | (0, 0.75, 0) | 50mm | Intimacy, focus |
| 03 — The Wall | (0, 1.65, -3.0) | (0, 1.8, -5.0) | 35mm | Discovery, memory |
| 04 — The Signal | (2.5, 1.65, -1.5) | (3.5, 1.8, -3.0) | 50mm | Mystery, transmission |
| 05 — The Shelves | (-2.5, 1.2, -1.0) | (-3.5, 1.5, -2.0) | 85mm | Knowledge, detail |
| 06 — The Experiment | (0, 1.65, 4.0) | (0, 1.5, 3.0) | 35mm | Wonder, exploration |
| 07 — The Window | (3.0, 1.65, -4.0) | (3.5, 2.0, -5.0) | 24mm | Outside world, scale |
| 08 — The Overview | (2.0, 2.5, 2.0) | (0, 1.0, -2.0) | 18mm | God view, spatial understanding |
| 09 — The Detail | (0.3, 0.9, 0.3) | (0, 0.75, 0) | 85mm | Micro-world, texture |
| 10 — The Exit | (0, 1.65, -6.0) | (0, 1.65, 8.0) | 35mm | Departure, longing |

### 8.4 Camera Movement

| Movement | Speed | Use Case |
|----------|-------|----------|
| Slow dolly | 0.3m/s | Approaching objects |
| Orbital | 10°/s | Exploring zones |
| Vertical shift | 0.2m/s | Standing/sitting transition |
| Focus pull | 1.0s | Directing attention |

---

## 9. BLENDER SCENE HIERARCHY

```
MVXWorld_Room/
├── ENVIRONMENT/
│   ├── Room_Shell/
│   │   ├── Walls
│   │   ├── Floor
│   │   ├── Ceiling
│   │   └── Windows
│   └── Architecture/
│       ├── Door_Frame
│       ├── Mouldings
│       └── Beams
├── ZONES/
│   ├── Central_Core/
│   │   ├── Desk_System
│   │   ├── Display_Array
│   │   ├── Chair
│   │   └── Desk_Props
│   ├── Memory_Wall/
│   │   ├── Floating_Frames
│   │   ├── Wall_Mounts
│   │   └── Decals
│   ├── Transmission_Zone/
│   │   ├── Holographic_Rig
│   │   ├── Signal_Devices
│   │   └── Data_Streams
│   ├── Archive_Shelves/
│   │   ├── Shelving_Units
│   │   ├── Books_Journals
│   │   └── Artifacts
│   └── Discovery_Zone/
│       ├── Experiment_Table
│       ├── Floating_Objects
│       └── Suspended_Mechanisms
├── PROPS/
│   ├── Books_[INSTANCE]
│   ├── Notes_[INSTANCE]
│   ├── Tools_[INSTANCE]
│   └── Artifacts_[UNIQUE]
├── LIGHTS/
│   ├── Natural/
│   │   ├── Sun
│   │   └── Window_Area
│   ├── Practical/
│   │   ├── Desk_Lamp
│   │   ├── Shelf_Strips
│   │   └── Holographic_Emission
│   └── FX/
│       ├── Volumetrics
│       └── Particle_Lights
├── FX/
│   ├── Dust_Particles
│   ├── Data_Streams
│   ├── Signal_Glow
│   └── Fog_Volume
├── CAMERA/
│   ├── Default_Exploration
│   ├── Cinematic_Shots/
│   │   ├── Shot_01_Arrival
│   │   ├── Shot_02_Desk
│   │   └── [...]
│   └── Interactive_Paths/
└── COLLECTIONS/
    ├── High_Detail
    ├── Medium_Detail
    ├── Low_Detail
    └── Instanced
```

### 9.1 Naming Conventions

| Category | Format | Example |
|----------|--------|---------|
| Meshes | `MESH_[Name]` | `MESH_Creation_Desk` |
| Materials | `MAT_[Name]` | `MAT_Aged_Walnut` |
| Textures | `TEX_[Name]_[Channel]` | `TEX_Walnut_BaseColor` |
| Lights | `LIGHT_[Type]_[Name]` | `LIGHT_Spot_DeskLamp` |
| Cameras | `CAM_[Name]` | `CAM_Default_Exploration` |
| Collections | `[ZONE]_[Subzone]` | `Central_Core_Desk` |

### 9.2 Instancing Strategy

| Asset Type | Strategy | Count |
|------------|----------|-------|
| Books | Collection instance + random transform | 20-30 |
| Notes/Paper | Instance + noise displacement | 10-15 |
| Tools | Instance + material variation | 8-12 |
| Floating Frames | Instance + unique content | 12-16 |
| Shelf Modules | Instance + slight rotation | 3-4 |

### 9.3 LOD Strategy

| LOD | Distance | Polycount | Texture Res |
|-----|----------|-----------|-------------|
| LOD0 | 0–3m | Full | 2K-4K |
| LOD1 | 3–8m | 50% | 1K-2K |
| LOD2 | 8m+ | 25% | 512-1K |

---

## 10. REAL-TIME OPTIMIZATION

### 10.1 Triangle Budgets

| Zone | Triangles | Draw Calls | Notes |
|------|-----------|------------|-------|
| Central Core | 50K-80K | 15-25 | Hero zone, highest detail |
| Memory Wall | 30K-50K | 20-30 | Many instances |
| Transmission Zone | 40K-60K | 10-15 | FX-heavy |
| Archive Shelves | 60K-90K | 25-40 | Dense props |
| Discovery Zone | 40K-70K | 15-25 | Mixed complexity |
| Environment | 20K-30K | 5-10 | Shell only |
| **TOTAL** | **240K-380K** | **90-145** | Target: <500K |

### 10.2 Draw Call Minimization

| Strategy | Implementation |
|----------|----------------|
| Texture atlasing | Combine materials per zone (1 atlas per 5-10 objects) |
| Material merging | Use UDIM for related objects |
| Instance batching | Same material + same mesh = GPU instancing |
| LOD switching | Automatic based on camera distance |
| Occlusion culling | Hide behind-wall objects |

### 10.3 Texture Atlas Layout

| Atlas | Contents | Resolution |
|-------|----------|------------|
| `ATLAS_CentralCore` | Desk, chair, displays, tools | 4K |
| `ATLAS_MemoryWall` | Frames, wall details, photos | 4K |
| `ATLAS_Transmission` | Rig, devices, screens | 2K |
| `ATLAS_ArchiveShelves` | Books, journals, artifacts | 4K |
| `ATLAS_DiscoveryZone` | Table, objects, mechanisms | 4K |
| `ATLAS_Environment` | Walls, floor, ceiling | 4K |

### 10.4 Lighting Strategy

| Element | Baked | Dynamic | Notes |
|---------|-------|---------|-------|
| Sun/Moon shadows | ✓ | — | Static for performance |
| Volumetrics | — | ✓ | Real-time for depth |
| Emissive surfaces | — | ✓ | Animated elements |
| Practical lights | ✓ | — | Consistent look |
| Ambient occlusion | ✓ | — | Texture-baked |

### 10.5 Eevee vs Cycles

| Use Case | Engine | Notes |
|----------|--------|-------|
| Real-time preview | Eevee | Fast iteration |
| Final render | Cycles | Quality + accurate GI |
| WebGL export | Eevee settings | Three.js compatibility |
| Baked lighting | Cycles → Eevee | Best of both |

### 10.6 WebGL Export Pipeline

| Step | Tool | Output |
|------|------|--------|
| 1. Scene prep | Blender | Clean hierarchy, UVs |
| 2. Material bake | Blender | PBR textures |
| 3. Export | glTF 2.0 | `.glb` or `.gltf` |
| 4. Optimize | gltf-transform | Draco compression |
| 5. Load | Three.js | `GLTFLoader` |
| 6. Render | Three.js | PBR + post-processing |

### 10.7 Particle & Fog Limits

| System | Max Count | Notes |
|--------|-----------|-------|
| Dust particles | 500-1000 | GPU instanced |
| Data stream particles | 200-500 | Shader-driven |
| Fog volume | 1 volume | VDB or shader |
| Signal glow | 10-20 emitters | Billboard or mesh |

---

## 11. ENVIRONMENTAL STORYTELLING

### 11.1 Hidden Narrative Elements

| Zone | Element | Location | Meaning |
|------|---------|----------|---------|
| Central Core | Coordinates etched on desk | Desk edge | Origin point |
| Central Core | Half-finished letter | Under papers | Unsent message |
| Central Core | Broken compass | Desk drawer | Lost direction |
| Memory Wall | Redacted photograph | Frame 3 | Hidden identity |
| Memory Wall | Map with X mark | Frame 7 | Destination |
| Memory Wall | Repeated symbol | Frames 2, 5, 12 | Recurring motif |
| Transmission | Glitched text fragment | Screen 1 | Incoming message |
| Transmission | Frequency number | Receiver | Tuning required |
| Transmission | Decoded message | Signal device | Partial truth |
| Archive | Book with marginalia | Shelf 2, row 3 | Active reader |
| Archive | Locked journal | Shelf 1 | Private thoughts |
| Archive | Unknown artifact | Shelf 3 | Foreign origin |
| Discovery | Working prototype | Experiment table | Active invention |
| Discovery | Blueprint with notes | Wall mount | Future plan |
| Discovery | Failed experiment | Corner | Learning process |

### 11.2 Storytelling Rules

1. **No exposition** — meaning is inferred, never stated
2. **Layered discovery** — first visit reveals surface, return visits reveal depth
3. **Consistent symbols** — 3-5 motifs recur across zones
4. **Implied chronology** — objects suggest sequence without timeline
5. **Personal artifacts** — handwriting, wear patterns, coffee rings

### 11.3 Symbol System

| Symbol | Meaning | Locations |
|--------|---------|-----------|
| Circle with dot | Origin/Self | Desk, wall, journal |
| Three parallel lines | Transmission | Screens, devices, notes |
| Broken circle | Incomplete/In-progress | Experiments, drafts |
| Arrow cluster | Direction/Navigation | Maps, blueprints |
| Frequency wave | Signal/Connection | Transmission zone |

---

## 12. EXTERNAL WORLD (WINDOWS)

### 12.1 Window Composition

Each window reveals MVXWorld beyond:

| Element | Description | Parallax Layer |
|---------|-------------|----------------|
| Floating landmasses | Architectural fragments in space | Background (0.1× speed) |
| Distant megastructures | Unknown purpose, scale | Mid-ground (0.3× speed) |
| Celestial anomalies | Subtle, not dominant | Background (0.05× speed) |
| Architectural debris | Broken walls, arches | Foreground (0.7× speed) |

### 12.2 Window-Specific Content

| Window | View | Mood |
|--------|------|------|
| North (Memory Wall) | Distant archive towers | Contemplative |
| East (Transmission) | Signal arrays, aurora | Active, mysterious |
| South (Discovery) | Floating experiments | Wonder, possibility |

### 12.3 Parallax Implementation

```
Layer 0 (sky): 0.0× camera movement
Layer 1 (far): 0.1× camera movement
Layer 2 (mid): 0.3× camera movement
Layer 3 (near): 0.7× camera movement
Layer 4 (room): 1.0× camera movement (base)
```

---

## 13. PRODUCTION WORKFLOW

### 13.1 Build Sequence

| Phase | Duration | Deliverables |
|-------|----------|--------------|
| 1. Blockout | 2-3 days | Graybox, scale verification |
| 2. Hero assets | 5-7 days | Desk, displays, holographic rig |
| 3. Zone dressing | 3-5 days | Props, furniture, details |
| 4. Materials | 3-4 days | PBR textures, shaders |
| 5. Lighting | 2-3 days | Natural + practical setup |
| 6. FX | 2-3 days | Particles, volumetrics |
| 7. Camera | 1-2 days | Shots, paths, DoF |
| 8. Optimization | 2-3 days | LODs, atlases, baking |
| 9. Export | 1-2 days | glTF, Three.js integration |
| **TOTAL** | **21-32 days** | Production-ready scene |

### 13.2 Quality Checkpoints

| Checkpoint | Criteria |
|------------|----------|
| Blockout review | Scale correct, zones defined |
| Asset review | Topology clean, UVs unwrapped |
| Material review | PBR values correct, imperfections present |
| Lighting review | Mood matches, no blown highlights |
| Performance review | Triangle budget met, draw calls optimized |
| Story review | Hidden elements placed, symbols consistent |

---

## 14. CREATIVE DIRECTIVE

### 14.1 The Room Is:

> "The first explorable node of MVXWorld."

### 14.2 Experience Goals

| Goal | Implementation |
|------|----------------|
| Curiosity | Objects invite investigation |
| Discovery | Hidden details reward exploration |
| Intimacy | Human-scale, personal objects |
| Wonder | External world confirms larger universe |
| Mystery | No complete explanations |

### 14.3 The Rule

> "Every object must imply a larger system beyond the room."

### 14.4 The Test

If a visitor says "I want to see more of this world" — success.  
If a visitor says "this is a cool room" — failure.

---

## APPENDIX A: REFERENCE IMAGES

| Reference | Use | Source |
|-----------|-----|--------|
| Study/Library rooms | Warmth, wood, books | Architectural Digest |
| Artist studios | Clutter, creativity, tools | Pinterest |
| Archive vaults | Order, mystery, preservation | Museum photography |
| Observatory windows | Scale, wonder, outside world | Sci-fi concept art |
| Antique shops | Patina, discovery, layers | Interior photography |

---

## APPENDIX B: TECHNICAL SPECS SUMMARY

| Spec | Value |
|------|-------|
| Blender version | 4.0+ |
| Render engines | Cycles (final) + Eevee (preview/export) |
| Export format | glTF 2.0 (.glb) |
| Target polycount | <500K triangles |
| Target draw calls | <150 |
| Texture budget | 6× 4K atlases + 10× 1K unique |
| Lighting | Baked + dynamic hybrid |
| Particle systems | 3-5 (GPU instanced) |
| Post-processing | Bloom, color grading, vignette |

---

## APPENDIX C: SUBDOMAIN ARCHITECTURE

| Subdomain | Purpose | Content |
|-----------|---------|---------|
| `room.mvxworld.art` | Main 3D experience | Three.js immersive room |
| `studio.mvxworld.art` | Creation hub | Interactive workbench |
| `archive.mvxworld.art` | Memory vault | Document/photo archive |
| `signal.mvxworld.art` | Transmission center | Live data streams |
| `explore.mvxworld.art` | Discovery zone | Experimental interface |

---

**Document Version:** 2.0  
**Last Updated:** 2026-06-13  
**Status:** Production-ready  
**Next Review:** Before Phase 1 build begins

---

*This specification is a living document. Update as build progresses.*
