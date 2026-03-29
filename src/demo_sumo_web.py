#!/usr/bin/env python3
"""
ПДД Demo: SUMO с веб-визуализацией.
Запускает SUMO headless + Python HTTP сервер с canvas-рендером.
Открывай http://localhost:8765
"""
import http.server
import json
import os
import socket
import threading
import time
import traci

SUMO_CFG = os.path.join(
    os.path.dirname(__file__), "..", "scenarios", "sumo_intersection", "intersection.sumocfg"
)

# Shared state
state = {"vehicles": [], "pedestrians": [], "traffic_lights": [], "step": 0}
lock = threading.Lock()


def run_sumo():
    """Run SUMO in background, update shared state."""
    sumo_bin = "sumo"
    traci.start([sumo_bin, "-c", SUMO_CFG, "--step-length", "0.1", "-e", "300"])
    print("SUMO started via TraCI")

    while True:
        try:
            traci.simulationStep()
        except traci.exceptions.FatalTraCIError:
            break

        vehicles = []
        for vid in traci.vehicle.getIDList():
            x, y = traci.vehicle.getPosition(vid)
            angle = traci.vehicle.getAngle(vid)
            vtype = traci.vehicle.getTypeID(vid)
            speed = traci.vehicle.getSpeed(vid)
            vehicles.append({"id": vid, "x": x, "y": y, "angle": angle, "type": vtype, "speed": speed})

        persons = []
        for pid in traci.person.getIDList():
            x, y = traci.person.getPosition(pid)
            angle = traci.person.getAngle(pid)
            persons.append({"id": pid, "x": x, "y": y, "angle": angle})

        tls = []
        for tlid in traci.trafficlight.getIDList():
            tl_state = traci.trafficlight.getRedYellowGreenState(tlid)
            tls.append({"id": tlid, "state": tl_state})

        with lock:
            state["vehicles"] = vehicles
            state["pedestrians"] = persons
            state["traffic_lights"] = tls
            state["step"] = traci.simulation.getTime()

        time.sleep(0.05)

    traci.close()


HTML = """<!DOCTYPE html>
<html>
<head>
<title>ПДД Simulator — SUMO</title>
<style>
  body { margin: 0; background: #1a1a1a; display: flex; justify-content: center; align-items: center; height: 100vh; font-family: system-ui; }
  canvas { border: 1px solid #333; }
  #info { position: fixed; top: 10px; left: 10px; color: #aaa; font-size: 14px; }
</style>
</head>
<body>
<div id="info">ПДД Simulator — SUMO | Step: <span id="step">0</span> | Vehicles: <span id="vcount">0</span></div>
<canvas id="c" width="800" height="800"></canvas>
<script>
const canvas = document.getElementById('c');
const ctx = canvas.getContext('2d');
const W = 800, H = 800;
// Map SUMO coords (-100..100) to canvas
const scale = 3.5;
const ox = W/2, oy = H/2;

function toCanvas(x, y) {
  return [ox + x * scale, oy - y * scale];
}

function drawRoad() {
  ctx.fillStyle = '#2a2a2a';
  ctx.fillRect(0, 0, W, H);
  // Grass
  ctx.fillStyle = '#2d5a1e';
  ctx.fillRect(0, 0, W, H);
  // NS road
  const roadW = 8 * scale;
  ctx.fillStyle = '#444';
  ctx.fillRect(ox - roadW/2, 0, roadW, H);
  // EW road
  ctx.fillRect(0, oy - roadW/2, W, roadW);
  // Lane markings
  ctx.strokeStyle = '#888';
  ctx.setLineDash([10, 10]);
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(ox, 0); ctx.lineTo(ox, oy - roadW/2);
  ctx.moveTo(ox, oy + roadW/2); ctx.lineTo(ox, H);
  ctx.moveTo(0, oy); ctx.lineTo(ox - roadW/2, oy);
  ctx.moveTo(ox + roadW/2, oy); ctx.lineTo(W, oy);
  ctx.stroke();
  ctx.setLineDash([]);
  // Crosswalks
  ctx.fillStyle = 'rgba(255,255,255,0.3)';
  for (let i = -3; i <= 3; i++) {
    ctx.fillRect(ox - roadW/2 - 2, oy + i*6 - 2, 4, 4);
    ctx.fillRect(ox + roadW/2 - 2, oy + i*6 - 2, 4, 4);
    ctx.fillRect(ox + i*6 - 2, oy - roadW/2 - 2, 4, 4);
    ctx.fillRect(ox + i*6 - 2, oy + roadW/2 - 2, 4, 4);
  }
}

function drawVehicle(v) {
  const [cx, cy] = toCanvas(v.x, v.y);
  const rad = -v.angle * Math.PI / 180;
  ctx.save();
  ctx.translate(cx, cy);
  ctx.rotate(rad);
  if (v.type === 'courier_bike') {
    // Bicycle - yellow
    ctx.fillStyle = '#FFD700';
    ctx.fillRect(-2, -5, 4, 10);
    // Backpack
    ctx.fillStyle = '#00CED1';
    ctx.fillRect(-3, -3, 6, 5);
  } else {
    // Car
    ctx.fillStyle = v.speed > 0.5 ? '#c0c0c0' : '#a04040';
    ctx.fillRect(-4, -8, 8, 16);
    // Windshield
    ctx.fillStyle = '#6688aa';
    ctx.fillRect(-3, -6, 6, 4);
  }
  ctx.restore();
}

function drawPerson(p) {
  const [cx, cy] = toCanvas(p.x, p.y);
  ctx.fillStyle = '#4488cc';
  ctx.beginPath();
  ctx.arc(cx, cy, 4, 0, Math.PI*2);
  ctx.fill();
}

function drawTrafficLight(tl) {
  // Show TL state as colored dots near intersection
  const colors = {'r': '#ff3333', 'y': '#ffcc00', 'G': '#33ff33', 'g': '#33ff33'};
  const x0 = ox + 120, y0 = 20;
  ctx.fillStyle = '#222';
  ctx.fillRect(x0 - 5, y0 - 5, tl.state.length * 15 + 10, 25);
  ctx.font = '10px monospace';
  ctx.fillStyle = '#888';
  ctx.fillText('TL: ' + tl.id, x0, y0 - 8);
  for (let i = 0; i < tl.state.length; i++) {
    ctx.fillStyle = colors[tl.state[i]] || '#666';
    ctx.beginPath();
    ctx.arc(x0 + i*15, y0 + 7, 5, 0, Math.PI*2);
    ctx.fill();
  }
}

async function update() {
  try {
    const res = await fetch('/state');
    const data = await res.json();
    drawRoad();
    data.vehicles.forEach(drawVehicle);
    data.pedestrians.forEach(drawPerson);
    data.traffic_lights.forEach(drawTrafficLight);
    document.getElementById('step').textContent = data.step.toFixed(1);
    document.getElementById('vcount').textContent = data.vehicles.length;
  } catch(e) {}
  requestAnimationFrame(update);
}
update();
</script>
</body>
</html>
"""


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/state":
            with lock:
                data = json.dumps(state)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(data.encode())
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(HTML.encode())

    def log_message(self, *args):
        pass  # silent


def find_port():
    with socket.socket() as s:
        s.bind(("", 0))
        return s.getsockname()[1]


if __name__ == "__main__":
    port = 8765
    print(f"Starting SUMO simulation...")

    sumo_thread = threading.Thread(target=run_sumo, daemon=True)
    sumo_thread.start()
    time.sleep(1)

    print(f"\n  ПДД Simulator → http://localhost:{port}\n")
    server = http.server.HTTPServer(("", port), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
