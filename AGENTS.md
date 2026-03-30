<!-- Updated: 2026-03-30 -->
# ПДД Simulator — Бишкек

Web-based 3D traffic rules simulator. Bishkek aesthetic. One HTML file, no build step.

## How It Works

```
index.html
  ├── loads GLTF/GLB models (Sketchfab realistic style)
  ├── builds scene: roads, buildings, vehicles, pedestrians
  ├── runs traffic light cycle (green→yellow→red, NS/EW alternating)
  ├── animates vehicles (stop on red, go on green, wrap at edges)
  └── 4 camera modes: overhead, driver, pedestrian, cinematic orbit
```

All scene data hardcoded in JS. JSON scenario configs exist in `scenarios/` but aren't wired up yet.

## Running

```bash
cd src/demo_threejs && python3 -m http.server 8767
```

## Visual Style: Sketchfab Realistic

**Decided:** all assets Sketchfab-sourced for style consistency. Kenney cartoon cars removed.

### Vehicles (PS1 low-poly realistic)
| Key | Model | Native max | Scale |
|---|---|---|---|
| `car_corolla` | Toyota Corolla PS1 | 11.5 | ×0.4 |
| `car_golf` | VW Golf PS1 | 20 | ×0.22 |
| `car_bmw` | BMW E46 | 289 | ×0.016 |
| `car_tahoe` | Chevy Tahoe PS1 | 3.2 | ×1.5 |
| `car_taxi` | Taxi stylized | 5.8 | ×0.8 |
| `car_van` | White Van PS1 | 2.7 | ×0.7 |
| `sf_bus_green` | Green city bus | 9.8 | ×1.2 |
| `sf_bus_modern` | Modern bus | 26 | ×0.4 |

### Buildings
| Key | Model | Native max | Scale |
|---|---|---|---|
| `sf_soviet_8k` | Soviet apartment (8K tex→resized 1K) | 1.7 | ×18 |
| `sf_panel` | Panel house 1970s | 179 | ×0.14 |
| `sf_khrush` | Khrushchevka small | 15 | ×2 |
| `office_bld` | Office building | 1.7 | ×12 |
| `glass_bld` | Glass tower | 2.9 | ×8 |
| `shop1` | Shop with awning | 19 | ×0.35 |

### Environment
- `poplar` — Poplar tree (Poly Pizza, ×0.7). Bishkek signature silhouette
- `sf_bus_stop_cozy` — Glass bus stop shelter (×1)
- `lp_people` — Lowpoly people group (×0.025)
- `bicycle` — Bicycle model (×0.02)
- KayKit props: streetlights, benches, bushes, hydrants, dumpsters

## Gotchas

- **Sketchfab models have wildly different scales** — always check bounding box in preview page before placing. Use `preview-ps1.html` / `preview-sf.html`
- **Sketchfab download needs API token** — `pass api/sketchfab`. Get from sketchfab.com/settings/password
- **soviet-apartment-8k was 158MB** — textures resized to 1K with `sips -Z 1024`. Don't re-download without resizing
- **khrushchevka-small 42MB** — same, resized to 1K
- **GLB files with external URI** (Kenney) need `models/Textures/colormap.png` at the right relative path
- **Russian road signs pack** loads as ONE object with ALL signs — needs Blender to extract individual signs
- **Bus stop shelter** ("BUS STOP") — needs Russian/Kyrgyz label, currently English

## Recipes

### Download a Sketchfab model
```bash
TOKEN=$(pass api/sketchfab)
ID="model-uuid-here"
NAME="my-model"
DIR="src/demo_threejs/models/sketchfab/$NAME"
mkdir -p "$DIR"
URL=$(curl -s "https://api.sketchfab.com/v3/models/$ID/download" \
  -H "Authorization: Token $TOKEN" | jq -r '.gltf.url')
curl -sL -o "$DIR/model.zip" "$URL"
cd "$DIR" && unzip -qo model.zip && rm model.zip
```

### Preview models before placing
Create/edit `preview-*.html` — loads models in a grid with OrbitControls and shows bounding box dimensions. Key for getting scale right.

### Add a model to the scene
1. Add to `manifest` array: `{n:'my_key', p:'models/sketchfab/my-model/scene.gltf'}`
2. In `build()`: `put('my_key', x, y, z, scale, rotationY)`
3. For moving: `mv.cars.push({ m: meshRef, ax:'z', sp:-5, lo:-65, hi:65, stop:[-8,0], dir:'ns' })`

## What's Not Done (P0→P2)

**P0:**
- Q3 pedestrian still barely visible — need a SINGLE PERSON model, not group. lp_people at 0.08 is a blob
- BUS STOP label → "Аялдама" / "Остановка"
- Vehicle turns (currently straight only)

**P1:**
- Each scenario needs visual QA — take screenshot, judge if scene matches question, fix positions. Use `visual-qa-loop` skill: audit all → batch fix → verify. MAX 3 ROUNDS.
- JSON config driving scene (configs exist, loader doesn't)
- T-junction second location
- More scenarios (10+, from real ПДД КР exam questions)

**P2:**
- Sound (engines, steps, signals)
- Mobile UI scaling
- Player-controlled driving
- Video recording (CCapture.js)
- React Three Fiber rewrite

## Docs

| Doc | What |
|---|---|
| `docs/bishkek-review-20260330.md` | 8 testers, 5.9/10. Key feedback |
| `docs/mvp-roadmap.md` | 5 location types, architecture target |
| `docs/bishkek-assets.md` | Asset wishlist with Sketchfab IDs |
| `docs/asset-packs.md` | All free asset sources catalog |
| `docs/preliminary-report.md` | Full research (AI video, CARLA, Godot, Three.js) |
| `docs/strategy.md` | Two-phase: Kling AI now + Three.js platform |

## Licenses

All assets CC0 or CC-BY. `license.txt` in each Sketchfab model dir.
Lowpoly people pack is CC-BY-NC-ND — check if OK for commercial education.
