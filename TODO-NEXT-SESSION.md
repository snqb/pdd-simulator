# Next Session — Camera Tuning

## What's done
- ✅ Nathan Walking pedestrian model (CC-BY, realistic, 21K faces)
- ✅ 10 quiz scenarios (ПДД КР exam questions)
- ✅ "Остановка / Аялдама" bus stop label
- ✅ Background peds hidden during quiz
- ✅ Traffic light "off" state
- ✅ Orbit controls during quiz (user can rotate camera)

## What needs fixing

### Camera positions for Q3, Q6, Q7
These 3 scenarios have cameras that clip into buildings (scene is dark).

**Root cause**: buildings at x=±30, sidewalks at x=±12, shops at x=14.  
Cameras must stay within the "street canyon" or be high enough to clear buildings.

**Working camera patterns** (copy these):
- Q1: `(14, 14, 14)` looking at `(0,0,0)` — diagonal from SE
- Q4: `(0, 18, 18)` looking at `(0,0,0)` — straight from south, high  

**Broken cameras to fix**:
- Q3 pedestrian: needs to see zebra at z=-8.5. Try: `(5, 18, 10)` → `(0, 0, -8)`
- Q6 right turn: needs to see zebra + Toyota at intersection. Try: `(5, 18, 10)` → `(-3, 0, -6)`
- Q7 overtake: needs truck at z=22 + Toyota at z=32. Try: `(5, 18, 40)` → `(-3, 0, 26)`

**Test method**: Open in REAL browser (not ABP), click through quiz, verify visually.
ABP headless is unreliable for timing (scenarios load slowly, clicks race).

### Nathan scale reference
- Native height: 185 units (centimeters)
- Scale 0.01 = 1.85m person (correct but HUGE at close camera)
- Scale 0.007 = 1.3m (good for background sidewalk)
- In quiz: scale 0.01 is fine but camera must be y=18+ to look DOWN at person

### Models downloaded but not wired
- `sf_traffic_light` — realistic Sketchfab traffic light (replaces KayKit)
- `people_standing` — group of 6 standing silhouettes (untextured)

## Local server
```bash
cd ~/Projects/pdd-simulator/src/demo_threejs && python3 -m http.server 19876
```
