# ПДД Simulator — Бишкек

Interactive traffic rules (ПДД) simulator for educational content. Web-based, Three.js.

## Stack

- **Three.js 0.170** — 3D rendering in browser, single HTML file
- **GLTF/GLB models** — Kenney (CC0), KayKit (CC0), Sketchfab (CC-BY), Poly Pizza (CC0)
- **No build step** — ES modules + importmap, served via any HTTP server
- **Future:** React Three Fiber for component architecture, SUMO for traffic physics

## Architecture

```
index.html (scene definition + animation loop)
├── models/               # Kenney + Poly Pizza GLBs
├── models/kaykit/         # KayKit City Builder GLTF
├── models/sketchfab/      # Sketchfab downloaded models
│   ├── soviet-apartment-8k/   # Хрущёвка с текстурами
│   ├── soviet-panel-house/    # Панельный дом
│   ├── khrushchevka-small/    # Маленькая хрущёвка
│   ├── modern-bus/            # Современный автобус
│   ├── green-bus/             # Зелёный автобус
│   └── poplar-tree-sf/        # Тополь
└── models/Textures/       # Kenney colormaps
```

## Key Decisions

- **Three.js over game engines** — runs in browser, zero install, dev-friendly
- **CC0/CC-BY assets** — no licensing issues for commercial education product
- **Bishkek vibe** — soviet apartment buildings, poplar trees, yellow waffle markings, green buses
- **Scene-as-code** — everything defined in JS, not visual editor → scriptable scenarios

## Model Scales (reference)

| Model | Native max | Scale → real | Notes |
|---|---|---|---|
| sf_soviet_8k | 1.7 | ×18 → 30m | Main хрущёвка |
| sf_panel | 179 | ×0.14 → 25m | Long panel house |
| sf_khrush | 15 | ×2 → 13m | Small khrushchevka |
| sf_bus_green | 9.8 | ×1.2 → 12m | City bus |
| sf_bus_modern | 26 | ×0.4 → 10m | Modern bus |
| Kenney cars | ~4 | ×1.8 → 7m | Sedan, taxi, SUV |
| poplar (PP) | ~13 | ×0.7 → 9m | Poplar tree |

## Running

```bash
cd src/demo_threejs
python3 -m http.server 8766
# → http://localhost:8766
```

## Docs

- `docs/preliminary-report.md` — full research report
- `docs/bishkek-assets.md` — asset catalog with download links
- `docs/asset-packs.md` — all free asset sources
- `docs/strategy.md` — two-phase strategy (Kling AI + Three.js)
- `docs/carla.md` — CARLA reference (future, GPU-only)
