# Next Session — DO THIS

## Context
`cd ~/Projects/pdd-simulator && python3 -m http.server 19876 --directory src/demo_threejs`
Live: https://snqb.github.io/pdd-simulator/

## P0 — Fix before anything else

### 1. Pedestrian model — VISIBLE, NOT low-poly blob
Current `lp_people` (Sketchfab lowpoly-people) is a group of blue silhouettes — invisible at scene scale.

Need: ONE realistic person model. Search Sketchfab:
- "realistic person walking" downloadable CC-BY
- "human character rigged" — Mixamo style
- NOT low-poly, NOT stylized — consistent with Sketchfab car/building style

Download with: `TOKEN=$(pass api/sketchfab)` + download recipe from AGENTS.md

### 2. Every question must match its scene — VISUAL QA LOOP
Use `visual-qa-loop` skill STRICTLY:
1. Screenshot all 5 questions (NO EDITS)
2. Write issue list per question: does scene match description? Y/N + why
3. Batch fix ALL positions/cameras/scales
4. Re-screenshot and verify
5. MAX 3 ROUNDS

Known issues from last session:
- Q1 (7/10): cars too far from intersection  
- Q2 (8/10): Toyota on waffle marking, should be before stop-line
- Q3 (5/10): **PEDESTRIAN NOT VISIBLE** — main P0
- Q4 (9/10): perfect, don't touch
- Q5 (8/10): Toyota partially hidden behind bus

### 3. BUS STOP → Остановка / Аялдама
The shelter model says "BUS STOP" in English. Either:
- Replace with different model
- Or overlay a 3D text sprite with Russian/Kyrgyz

## P1 — After P0 is done

### 4. More scenarios (10 total)
Add 5 more from real ПДД КР exam:
- Right turn with pedestrian
- Roundabout priority  
- T-junction yield
- Overtaking rules
- Night/rain conditions

### 5. Style consistency
All models should look realistic (Sketchfab style), NOT cartoon/low-poly.
Current cartoon elements to replace:
- KayKit traffic lights → find Sketchfab realistic ones
- KayKit props (benches, hydrants) → OK for now, low priority

## Rules for next session
- **ABP browser testing** — always verify visually
- **visual-qa-loop** — structured, not infinite circle
- **Commit after each fix** — not after 50 changes
- **Push to prod** — GitHub Pages auto-deploys on push
