# MVXWorld — Active Tasks

## Error Page System

**Status:** COMPLETE  
**Completed:** 2026-06-13

| Page | Code | MVXWorld Name | Signal Status | Display | Kicker |
|------|------|---------------|---------------|---------|--------|
| `404.html` | 404 | /lost | signal lost | l*o*st. | you walked into an unmapped frequency |
| `500.html` | 500 | /error | signal corrupted | br*ea*k. | the transmission collapsed mid-sentence |
| `502.html` | 502 | /interference | frequency interference | cl*as*h. | two signals collided in the wire |
| `503.html` | 503 | /offline | transmission offline | bl*ac*k. | the room is temporarily dark |
| `504.html` | 504 | /timeout | signal timeout | w*ai*t. | the response never arrived |
| `403.html` | 403 | /locked | frequency locked | l*oc*k. | this room requires a different key |
| `401.html` | 401 | /unknown | identity required | wh*o*? | the world doesn't recognize you yet |
| `429.html` | 429 | /overload | signal overload | sl*ow*. | too many transmissions at once |

### Features
- All pages use `tokens.css` for design system
- Grain texture overlay
- Acid green + burn accents
- Cormorant Garamond italic + IBM Plex Mono
- Fade-to-black page transitions
- IntersectionObserver reveals
- Reduced motion support
- 503 has 30s auto-retry countdown
- 429 has 15s auto-retry countdown
- All pages have "known frequencies" directory (500, 502, 504)
- Technical detail sections explain what happened

---

## 3D Build (In Progress)

## Phase 1: Foundation

**Status:** IN PROGRESS  
**Started:** 2026-06-13

### Completed
- [x] Create enhanced 3D prompt (`MVXWORLD_3D_PROMPT_ENHANCED.md`)
- [x] Create implementation plan (`3D_IMPLEMENTATION_PLAN.md`)
- [x] Save build plan to tasks (`tasks/3D_BUILD_PLAN.md`)
- [x] Set up 3D project directory structure
- [x] Create Blender graybox script (`3d/blender/scripts/graybox_blockout.py`)
- [x] Create Creation Desk script (`3d/blender/scripts/creation_desk.py`)
- [x] Create Memory Wall script (`3d/blender/scripts/memory_wall.py`)
- [x] Create Transmission Zone script (`3d/blender/scripts/transmission_zone.py`)
- [x] Create Archive Shelves script (`3d/blender/scripts/archive_shelves.py`)
- [x] Create Discovery Zone script (`3d/blender/scripts/discovery_zone.py`)
- [x] Create master build script (`3d/blender/scripts/build_all.py`)

### Pending
- [ ] Run `build_all.py` in Blender
- [ ] Review generated scene
- [ ] Test camera positions
- [ ] Add textures and UV unwrapping
- [ ] Test glTF export pipeline
- [ ] Set up Three.js project

---

## Blender Scripts Available

| Script | Zone | Objects | Status |
|--------|------|---------|--------|
| `build_all.py` | MASTER | All zones | ✓ Ready |
| `graybox_blockout.py` | All | Room shell | ✓ Complete |
| `creation_desk.py` | Central Core | Desk + props | ✓ Complete |
| `memory_wall.py` | Memory Wall | Frames + symbols | ✓ Complete |
| `transmission_zone.py` | Transmission | Rig + devices | ✓ Complete |
| `archive_shelves.py` | Archive | Shelves + books | ✓ Complete |
| `discovery_zone.py` | Discovery | Experiments | ✓ Complete |

---

## Quick Start — One Click Build

1. Open **Blender 4.0+**
2. Go to **Scripting** workspace
3. Open `3d/blender/scripts/build_all.py`
4. Click **Run Script**
5. Wait 2-5 minutes
6. Save as `3d/blender/scenes/MVXWorld_Room.blend`

The master script will:
- Clean the default scene
- Build all 6 zones
- Set up lighting and cameras
- Configure render settings
- Print scene statistics

---

## What Gets Built

### Central Core (Creation Desk)
- Desk surface (aged walnut)
- Drawer units (left + right)
- Desk legs (brushed metal)
- Back panel + shelves
- Monitor arm mount
- Coffee cup, pens, notebook
- Articulated desk lamp
- Cable management

### Memory Wall
- 16 floating frames
- Circle-dot symbols (×3)
- Parallel line groups (×2)
- Broken circle symbols (×2)
- Wall lighting strip
- Spot lights
- Amsterdam coordinates

### Transmission Zone
- Holographic projection rig
- Signal receiver device
- Frequency display
- Waveform visualization
- Data stream emitters
- Transmission tablets
- Signal orbs

### Archive Shelves
- 3 shelving units
- 30 books
- 8 journals
- 12 artifacts
- 4 miniature world models
- 3 specimen jars
- Shelf lighting

### Discovery Zone
- Experiment workbench
- Floating geometric objects (8)
- Half-finished inventions (3)
- Abstract devices (4)
- Physics mechanisms (2)
- Suspended forms (5)
- Tool rack + tools (10)

---

## Next Session Tasks

1. Run `build_all.py` in Blender
2. Review generated scene
3. Adjust zone positions if needed
4. Add textures and UV unwrapping
5. Test render (F12)
6. Export test → Three.js

---

*Updated: 2026-06-13*
