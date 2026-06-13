# MVXWorld 3D Implementation Plan

## Phase 1: Foundation (Weeks 1-2)

### Infrastructure Setup

```
mvxworld-art/
├── 3d/                          # 3D source files
│   ├── blender/                 # Blender project files
│   │   ├── scenes/
│   │   ├── assets/
│   │   ├── textures/
│   │   └── exports/
│   └── threejs/                 # Three.js implementation
│       ├── src/
│       ├── public/
│       └── package.json
├── room.mvxworld.art/           # 3D experience subdomain
│   ├── index.html
│   ├── assets/
│   └── js/
└── studio.mvxworld.art/         # Creation hub subdomain
    ├── index.html
    └── js/
```

### Subdomain Strategy

| Subdomain | Hosting | Purpose |
|-----------|---------|---------|
| `room.mvxworld.art` | Cloudflare Pages | Main 3D experience |
| `studio.mvxworld.art` | Cloudflare Pages | Interactive creation |
| `archive.mvxworld.art` | Cloudflare Pages | Document vault |
| `signal.mvxworld.art` | Cloudflare Workers | Live data streams |
| `explore.mvxworld.art` | Cloudflare Pages | Experimental UI |

---

## Phase 2: Blender Build (Weeks 3-6)

### Week 3-4: Blockout + Hero Assets

**Day 1-3: Graybox**
```
- Room shell (walls, floor, ceiling)
- Window openings
- Zone boundaries (tape on floor)
- Scale verification with human figure
```

**Day 4-7: Hero Assets**
```
- Creation Desk (highest priority)
- Display Array
- Holographic Rig
- Archive Shelving (×3)
```

### Week 5-6: Dressing + Materials

**Day 8-10: Medium Assets**
```
- Chair, books, journals
- Floating frames
- Tools, artifacts
- Experiment objects
```

**Day 11-14: Materials**
```
- Aged walnut wood shader
- Brushed metal shader
- Imperfect glass shader
- Paper/leather shaders
- Emission materials (acid green)
```

---

## Phase 3: Lighting + FX (Weeks 7-8)

### Lighting Setup

```
Natural:
├── Sun lamp (35° elevation)
├── Window area lights (×3)
└── HDRI environment

Practical:
├── Desk lamp (warm, 2700K)
├── Shelf strips (cool, 3000K)
└── Holographic emission (acid)

Volumetric:
├── Fog volume (density 0.03)
├── Dust particles (GPU instanced)
└── Light shafts through windows
```

### FX Systems

| System | Type | Count | Notes |
|--------|------|-------|-------|
| Dust | Particle | 500 | GPU instanced |
| Data stream | Shader | 3-5 | UV scroll |
| Signal glow | Emission | 10 | Billboard |
| Fog | Volume | 1 | VDB or shader |

---

## Phase 4: Camera + Export (Weeks 9-10)

### Camera System

```
Default:
├── Position: (0, 1.65, 5.0)
├── Lens: 35mm
├── Aperture: f/2.8
└── Focus: 3.0m

Cinematic Shots:
├── Shot 01: Arrival (24mm, f/8)
├── Shot 02: Desk (50mm, f/2.0)
├── Shot 03: Wall (35mm, f/4.0)
├── Shot 04: Signal (50mm, f/2.8)
├── Shot 05: Shelves (85mm, f/2.0)
├── Shot 06: Experiment (35mm, f/4.0)
├── Shot 07: Window (24mm, f/8)
├── Shot 08: Overview (18mm, f/11)
├── Shot 09: Detail (85mm, f/1.4)
└── Shot 10: Exit (35mm, f/4.0)
```

### Export Pipeline

```
Blender → glTF 2.0 (.glb)
  ├── Draco compression
  ├── Texture optimization
  └── LOD generation

Three.js → WebGL
  ├── GLTFLoader
  ├── PBR materials
  ├── Post-processing (bloom, color grade)
  └── Camera controls
```

---

## Phase 5: Three.js Integration (Weeks 11-12)

### Three.js Architecture

```javascript
// Main scene structure
MVXWorld/
├── Scene.js          // Main scene setup
├── Camera.js         // Camera system
├── Lights.js         // Lighting setup
├── Loader.js         // Asset loading
├── Controls.js       // User input
├── PostProcessing.js // Effects
├── Zones/
│   ├── CentralCore.js
│   ├── MemoryWall.js
│   ├── TransmissionZone.js
│   ├── ArchiveShelves.js
│   └── DiscoveryZone.js
└── FX/
    ├── Particles.js
    ├── Fog.js
    └── Emission.js
```

### Performance Targets

| Metric | Target | Notes |
|--------|--------|-------|
| FPS | 60 | Desktop |
| FPS | 30 | Mobile |
| Load time | <5s | Initial load |
| Memory | <512MB | GPU memory |
| Triangles | <500K | Total scene |
| Draw calls | <150 | Optimized |

---

## Phase 6: Deployment (Week 13)

### DNS Configuration

```
Type  | Name    | Value                    | TTL
CNAME | room    | mvxworld-3d.pages.dev    | 1 hour
CNAME | studio  | mvxworld-studio.pages.dev | 1 hour
CNAME | archive | mvxworld-archive.pages.dev | 1 hour
CNAME | signal  | mvxworld-signal.workers.dev | 1 hour
CNAME | explore | mvxworld-explore.pages.dev | 1 hour
```

### Cloudflare Pages Setup

```bash
# Room subdomain
cd 3d/threejs
npm run build
wrangler pages deploy dist --project-name=mvxworld-3d

# Studio subdomain
cd ../../studio.mvxworld.art
wrangler pages deploy . --project-name=mvxworld-studio
```

### Performance Monitoring

```
Cloudflare Analytics:
├── Page load times
├── Core Web Vitals
├── Error rates
└── Geographic distribution

Custom Metrics:
├── 3D render performance
├── Asset load times
├── Interaction events
└── Zone navigation
```

---

## Technical Stack

### Blender Pipeline

| Tool | Version | Purpose |
|------|---------|---------|
| Blender | 4.0+ | 3D modeling/rendering |
| Cycles | — | Final render engine |
| Eevee | — | Real-time preview |
| glTF Exporter | Built-in | Web export |

### Three.js Pipeline

| Tool | Version | Purpose |
|------|---------|---------|
| Three.js | r160+ | WebGL renderer |
| GLTFLoader | — | Asset loading |
| DRACOLoader | — | Mesh compression |
| EffectComposer | — | Post-processing |
| Vite | 5.x | Build tool |

### Hosting

| Service | Purpose | Cost |
|---------|---------|------|
| Cloudflare Pages | Static hosting | Free |
| Cloudflare Workers | API/auth | Free tier |
| Cloudflare R2 | Asset storage | Free tier |
| GitHub | Source control | Free |

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Visual fidelity | 90%+ | Artist review |
| Performance | 60fps | Chrome DevTools |
| Load time | <5s | Lighthouse |
| Accessibility | WCAG 2.1 AA | axe-core |
| Story discovery | 80%+ | User testing |

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Performance issues | LOD system, texture atlasing |
| Mobile compatibility | Responsive 3D, touch controls |
| Load times | Progressive loading, compression |
| Browser support | WebGL 2.0 fallback |
| Asset size | Draco compression, texture optimization |

---

## Next Steps

1. [ ] Review enhanced prompt (`MVXWORLD_3D_PROMPT_ENHANCED.md`)
2. [ ] Set up Blender project structure
3. [ ] Begin graybox blockout
4. [ ] Test Three.js pipeline with simple scene
5. [ ] Configure Cloudflare subdomains

---

**Document Version:** 1.0  
**Created:** 2026-06-13  
**Status:** Ready for execution
