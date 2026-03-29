#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["metadrive-simulator"]
# ///
"""
ПДД Demo: MetaDrive — перекрёсток, машина, трафик.
Запуск: uv run demo_metadrive.py
"""
from metadrive.envs.metadrive_env import MetaDriveEnv
from metadrive.component.map.base_map import BaseMap
from metadrive.component.map.pg_map import MapGenerateMethod
import time

env = MetaDriveEnv(dict(
    map_config={
        BaseMap.GENERATE_TYPE: MapGenerateMethod.BIG_BLOCK_SEQUENCE,
        BaseMap.GENERATE_CONFIG: "X",  # X = crossroad
        BaseMap.LANE_WIDTH: 3.7,
        BaseMap.LANE_NUM: 2,
    },
    traffic_density=0.3,
    random_traffic=True,
    use_render=True,
    window_size=(1280, 720),
    show_interface=True,
    show_fps=True,
    num_scenarios=1,
    start_seed=42,
))

try:
    obs, info = env.reset()
    print("MetaDrive intersection loaded!")
    print("Controls: WASD to drive, mouse to look")
    for step in range(3000):
        action = [0.0, 0.3]
        obs, reward, terminated, truncated, info = env.step(action)
        if terminated or truncated:
            obs, info = env.reset()
        time.sleep(0.02)
finally:
    env.close()
