# MVXWorld 3D Build Plan

## Master Documents

| Document | Location | Purpose |
|----------|----------|---------|
| Enhanced Prompt | `MVXWORLD_3D_PROMPT_ENHANCED.md` | Full build specification |
| Implementation Plan | `3D_IMPLEMENTATION_PLAN.md` | 13-week roadmap |
| This File | `tasks/3D_BUILD_PLAN.md` | Active tracking |

---

## Current Phase: Phase 1 — Foundation

**Status:** IN PROGRESS  
**Started:** 2026-06-13  
**Target:** Week 2

### Tasks

- [ ] Set up Blender project structure
- [ ] Create graybox blockout of room shell
- [ ] Verify scale with human figure
- [ ] Test Three.js pipeline with simple export
- [ ] Configure `room.mvxworld.art` subdomain

---

## Build Sequence

| Phase | Weeks | Status |
|-------|-------|--------|
| 1. Foundation | 1-2 | IN PROGRESS |
| 2. Blender Build | 3-6 | PENDING |
| 3. Lighting + FX | 7-8 | PENDING |
| 4. Camera + Export | 9-10 | PENDING |
| 5. Three.js Integration | 11-12 | PENDING |
| 6. Deployment | 13 | PENDING |

---

## Blender Project Structure

```
3d/
├── blender/
│   ├── scenes/
│   │   ├── MVXWorld_Room.blend    # Main scene
│   │   ├── MVXWorld_Assets.blend  # Asset library
│   │   └── MVXWorld_Materials.blend # Material library
│   ├── assets/
│   │   ├── textures/
│   │   ├── hdri/
│   │   └── reference/
│   └── exports/
│       ├── glb/
│       └── usdz/
└── threejs/
    ├── src/
    ├── public/
    └── package.json
```

---

## Asset Priority List

### Hero Assets (Build First)

| Asset | Zone | Polycount | Status |
|-------|------|-----------|--------|
| Creation Desk | Central Core | 8K-12K | PENDING |
| Display Array | Central Core | 4K each | PENDING |
| Holographic Rig | Transmission | 10K-15K | PENDING |
| Archive Shelving (×3) | Archive | 6K each | PENDING |
| Experiment Table | Discovery | 5K-8K | PENDING |

### Medium Assets

| Asset | Zone | Polycount | Status |
|-------|------|-----------|--------|
| Desk Chair | Central Core | 4K-6K | PENDING |
| Floating Frames (×16) | Memory Wall | 1K each | PENDING |
| Books (×30) | Archive | 500 each | PENDING |
| Desk Lamp | Central Core | 3K | PENDING |
| Signal Device | Transmission | 5K | PENDING |

### Small Props

| Asset | Zone | Polycount | Status |
|-------|------|-----------|--------|
| Coffee Cup | Central Core | 800 | PENDING |
| Notes/Paper (×15) | All | 200 each | PENDING |
| Tools (×12) | Central Core | 500-1K | PENDING |
| Artifacts (×12) | Archive | 1K-2K | PENDING |
| Geometric Objects (×8) | Discovery | 2K-4K | PENDING |

---

## Material Priority

| Material | Use | Status |
|----------|-----|--------|
| Aged Walnut | Desk, shelves, table | PENDING |
| Brushed Metal | Hardware, fixtures | PENDING |
| Imperfect Glass | Windows, displays | PENDING |
| Paper | Notes, books, sketches | PENDING |
| Worn Leather | Chair, journals | PENDING |
| Emissive Holographic | Transmission zone | PENDING |
| Stone | Floor accent | PENDING |
| Brass | Lamp, hardware | PENDING |

---

## Lighting Setup

### Natural Light

```
Sun:
├── Type: Sun
├── Angle: 35° elevation, 220° azimuth
├── Intensity: 80,000-100,000 lux
├── Color: 5500K (day) / 8000K (night)
└── Shadows: Soft, ray-traced

Windows:
├── Type: Area lights (×3)
├── Intensity: 15,000 lux
├── Color: 5500K
└── Volumetric shafts: Yes
```

### Practical Lights

```
Desk Lamp:
├── Type: Spot
├── Intensity: 800 lumens
├── Color: 2700K (warm)
└── Position: Creation Core

Shelf Strips:
├── Type: Area
├── Intensity: 200 lumens/m
├── Color: 3000K
└── Position: Archive Shelves

Holographic:
├── Type: Emission
├── Strength: 4.0-6.0
├── Color: #c8ff00 (acid)
└── Position: Transmission Zone
```

---

## Camera Shots

| # | Name | Position | Lens | Aperture |
|---|------|----------|------|----------|
| 01 | Arrival | (0, 1.65, 8.0) | 24mm | f/8 |
| 02 | Desk | (1.5, 1.15, 1.5) | 50mm | f/2.0 |
| 03 | Wall | (0, 1.65, -3.0) | 35mm | f/4.0 |
| 04 | Signal | (2.5, 1.65, -1.5) | 50mm | f/2.8 |
| 05 | Shelves | (-2.5, 1.2, -1.0) | 85mm | f/2.0 |
| 06 | Experiment | (0, 1.65, 4.0) | 35mm | f/4.0 |
| 07 | Window | (3.0, 1.65, -4.0) | 24mm | f/8 |
| 08 | Overview | (2.0, 2.5, 2.0) | 18mm | f/11 |
| 09 | Detail | (0.3, 0.9, 0.3) | 85mm | f/1.4 |
| 10 | Exit | (0, 1.65, -6.0) | 35mm | f/4.0 |

---

## Performance Targets

| Metric | Target | Notes |
|--------|--------|-------|
| Total triangles | <500K | All zones |
| Draw calls | <150 | Optimized |
| Texture budget | 6× 4K atlases | + 10× 1K unique |
| FPS (desktop) | 60 | Chrome/Firefox |
| FPS (mobile) | 30 | iOS Safari |
| Load time | <5s | Initial |
| Memory | <512MB | GPU |

---

## Subdomain Architecture

| Subdomain | Purpose | Hosting |
|-----------|---------|---------|
| `room.mvxworld.art` | Main 3D experience | Cloudflare Pages |
| `studio.mvxworld.art` | Creation hub | Cloudflare Pages |
| `archive.mvxworld.art` | Memory vault | Cloudflare Pages |
| `signal.mvxworld.art` | Data streams | Cloudflare Workers |
| `explore.mvxworld.art` | Experimental UI | Cloudflare Pages |

---

## Next Actions

1. **Create Blender project** at `3d/blender/scenes/MVXWorld_Room.blend`
2. **Start graybox blockout** — room shell, windows, zone boundaries
3. **Add human figure** for scale verification
4. **Test export** — simple cube → glTF → Three.js
5. **Commit structure** to git

---

*Updated: 2026-06-13*
