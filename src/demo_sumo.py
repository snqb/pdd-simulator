#!/usr/bin/env python3
"""
ПДД Demo: SUMO — перекрёсток со светофором, машины, пешеходы.
Генерирует конфиги и запускает SUMO-GUI.

Запуск: python3 demo_sumo.py
"""
import os
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
SUMO_DIR = os.path.join(BASE, "..", "scenarios", "sumo_intersection")
os.makedirs(SUMO_DIR, exist_ok=True)

# 1. Node file (intersection geometry)
nodes_xml = """<?xml version="1.0" encoding="UTF-8"?>
<nodes>
    <!-- Center intersection -->
    <node id="C" x="0" y="0" type="traffic_light"/>

    <!-- Arms of the intersection -->
    <node id="N" x="0" y="100"/>
    <node id="S" x="0" y="-100"/>
    <node id="E" x="100" y="0"/>
    <node id="W" x="-100" y="0"/>
</nodes>
"""

# 2. Edge file (roads connecting nodes)
edges_xml = """<?xml version="1.0" encoding="UTF-8"?>
<edges>
    <!-- North-South -->
    <edge id="NC" from="N" to="C" numLanes="2" speed="13.89"/>
    <edge id="CN" from="C" to="N" numLanes="2" speed="13.89"/>
    <edge id="SC" from="S" to="C" numLanes="2" speed="13.89"/>
    <edge id="CS" from="C" to="S" numLanes="2" speed="13.89"/>

    <!-- East-West -->
    <edge id="EC" from="E" to="C" numLanes="2" speed="13.89"/>
    <edge id="CE" from="C" to="E" numLanes="2" speed="13.89"/>
    <edge id="WC" from="W" to="C" numLanes="2" speed="13.89"/>
    <edge id="CW" from="C" to="W" numLanes="2" speed="13.89"/>
</edges>
"""

# 3. Route file (traffic demand — cars + pedestrians)
routes_xml = """<?xml version="1.0" encoding="UTF-8"?>
<routes>
    <!-- Vehicle types -->
    <vType id="car" accel="2.6" decel="4.5" length="4.5" maxSpeed="13.89" color="0.7,0.7,0.7"/>
    <vType id="courier_bike" vClass="bicycle" accel="1.2" decel="3.0" length="1.8" maxSpeed="6.0" color="1.0,0.9,0.0"/>

    <!-- Car flows from each direction -->
    <flow id="flow_SC" type="car" from="SC" to="CN" begin="0" end="120" probability="0.15"/>
    <flow id="flow_NC" type="car" from="NC" to="CS" begin="0" end="120" probability="0.10"/>
    <flow id="flow_EC" type="car" from="EC" to="CW" begin="0" end="120" probability="0.12"/>
    <flow id="flow_WC" type="car" from="WC" to="CE" begin="0" end="120" probability="0.08"/>

    <!-- Turning traffic -->
    <flow id="flow_SC_turn" type="car" from="SC" to="CE" begin="0" end="120" probability="0.05"/>
    <flow id="flow_EC_turn" type="car" from="EC" to="CN" begin="0" end="120" probability="0.05"/>

    <!-- Courier on bicycle -->
    <flow id="courier" type="courier_bike" from="EC" to="CW" begin="5" end="60" probability="0.08"/>

    <!-- Pedestrians -->
    <personFlow id="peds_NS" begin="0" end="120" probability="0.1">
        <walk from="NC" to="CS"/>
    </personFlow>
    <personFlow id="peds_EW" begin="0" end="120" probability="0.08">
        <walk from="EC" to="CW"/>
    </personFlow>
</routes>
"""

# 4. SUMO config
sumo_cfg = """<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <input>
        <net-file value="intersection.net.xml"/>
        <route-files value="routes.rou.xml"/>
    </input>
    <time>
        <begin value="0"/>
        <end value="120"/>
    </time>
    <processing>
        <pedestrian.model value="striping"/>
    </processing>
    <gui_only>
        <gui-settings-file value="view.xml"/>
    </gui_only>
</configuration>
"""

# 5. GUI view settings (3D-like top view)
view_xml = """<?xml version="1.0" encoding="UTF-8"?>
<viewsettings>
    <viewport x="0" y="0" zoom="300"/>
    <scheme name="real world"/>
    <delay value="50"/>
</viewsettings>
"""

# Write all files
files = {
    "intersection.nod.xml": nodes_xml,
    "intersection.edg.xml": edges_xml,
    "routes.rou.xml": routes_xml,
    "intersection.sumocfg": sumo_cfg,
    "view.xml": view_xml,
}

for name, content in files.items():
    path = os.path.join(SUMO_DIR, name)
    with open(path, "w") as f:
        f.write(content)
    print(f"  Created {name}")

# 6. Build network
print("\nBuilding road network...")
netconvert = os.path.join(os.environ.get("SUMO_HOME", ""), "bin", "netconvert")
if not os.path.exists(netconvert):
    netconvert = "netconvert"  # try PATH

subprocess.run([
    netconvert,
    "--node-files", os.path.join(SUMO_DIR, "intersection.nod.xml"),
    "--edge-files", os.path.join(SUMO_DIR, "intersection.edg.xml"),
    "--output-file", os.path.join(SUMO_DIR, "intersection.net.xml"),
    "--tls.guess", "true",
    "--sidewalks.guess", "true",
    "--crossings.guess", "true",
], check=True)
print("Network built!")

# 7. Launch SUMO-GUI
print("\nLaunching SUMO GUI...")
print("(Close the SUMO window to exit)")

sumo_gui = os.path.join(os.environ.get("SUMO_HOME", ""), "bin", "sumo-gui")
if not os.path.exists(sumo_gui):
    sumo_gui = "sumo-gui"

subprocess.run([
    sumo_gui,
    "-c", os.path.join(SUMO_DIR, "intersection.sumocfg"),
], check=True)
