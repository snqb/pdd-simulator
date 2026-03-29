#!/usr/bin/env python3
"""
ПДД Сценарий: Перекрёсток с курьером.

Сцена: машина на перекрёстке, курьер на велосипеде,
пешеходы на тротуаре, светофор зелёный.

Требования: CARLA 0.10.0 сервер.
Запуск: python3 scenario_intersection.py --host GPU_SERVER_IP
"""

import argparse
import carla
import math
import os
import time


def main():
    parser = argparse.ArgumentParser(description="ПДД: Перекрёсток")
    parser.add_argument("--host", default="localhost", help="CARLA server host")
    parser.add_argument("--port", default=2000, type=int, help="CARLA server port")
    parser.add_argument("--map", default="Town10", help="Map name")
    parser.add_argument("--duration", default=15, type=int, help="Scene duration (sec)")
    parser.add_argument("--output", default="output", help="Output dir for frames")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    actors = []

    try:
        # --- Connect ---
        client = carla.Client(args.host, args.port)
        client.set_timeout(10.0)
        world = client.load_world(args.map)
        bp_lib = world.get_blueprint_library()
        map_ = world.get_map()

        # --- Weather: sunny day ---
        world.set_weather(carla.WeatherParameters.ClearNoon)

        # --- Find intersection spawn points ---
        spawn_points = map_.get_spawn_points()
        # Pick a spawn near an intersection (heuristic: close waypoints with junction flag)
        junction_spawns = []
        for sp in spawn_points:
            wp = map_.get_waypoint(sp.location)
            if wp.is_junction:
                junction_spawns.append(sp)

        if not junction_spawns:
            junction_spawns = spawn_points[:5]

        car_spawn = junction_spawns[0]

        # --- Spawn car (sedan) ---
        car_bp = bp_lib.find("vehicle.lincoln.mkz_2020")
        car = world.spawn_actor(car_bp, car_spawn)
        actors.append(car)
        print(f"Car spawned at {car_spawn.location}")

        # --- Spawn cyclist ---
        bike_bp = bp_lib.find("vehicle.bh.crossbike")
        bike_spawn = carla.Transform(
            carla.Location(
                x=car_spawn.location.x + 5,
                y=car_spawn.location.y + 3,
                z=car_spawn.location.z,
            ),
            car_spawn.rotation,
        )
        cyclist = world.try_spawn_actor(bike_bp, bike_spawn)
        if cyclist:
            actors.append(cyclist)
            print(f"Cyclist spawned")

        # --- Spawn pedestrians ---
        walker_bps = bp_lib.filter("walker.pedestrian.*")
        walker_controller_bp = bp_lib.find("controller.ai.walker")

        for i in range(3):
            wb = walker_bps[i % len(walker_bps)]
            walker_spawn = carla.Transform(
                carla.Location(
                    x=car_spawn.location.x + 8 + i * 2,
                    y=car_spawn.location.y - 5,
                    z=car_spawn.location.z + 1,
                )
            )
            walker = world.try_spawn_actor(wb, walker_spawn)
            if walker:
                actors.append(walker)
                # AI controller
                controller = world.spawn_actor(walker_controller_bp, carla.Transform(), walker)
                actors.append(controller)
                controller.start()
                # Walk to a point across the street
                target = carla.Location(
                    x=walker_spawn.location.x + 20,
                    y=walker_spawn.location.y + 10,
                    z=walker_spawn.location.z,
                )
                controller.go_to_location(target)
                controller.set_max_speed(1.4)  # normal walking speed
                print(f"Pedestrian {i+1} spawned")

        # --- Camera: overhead (bird's eye) ---
        cam_bp = bp_lib.find("sensor.camera.rgb")
        cam_bp.set_attribute("image_size_x", "1920")
        cam_bp.set_attribute("image_size_y", "1080")
        cam_bp.set_attribute("fov", "90")

        cam_transform = carla.Transform(
            carla.Location(
                x=car_spawn.location.x + 5,
                y=car_spawn.location.y,
                z=car_spawn.location.z + 25,  # 25m above
            ),
            carla.Rotation(pitch=-70, yaw=car_spawn.rotation.yaw),  # looking down
        )
        camera = world.spawn_actor(cam_bp, cam_transform)
        actors.append(camera)

        # Save frames
        frame_count = [0]

        def save_frame(image):
            path = os.path.join(args.output, f"{frame_count[0]:06d}.png")
            image.save_to_disk(path)
            frame_count[0] += 1

        camera.listen(save_frame)
        print(f"Camera recording to {args.output}/")

        # --- Start recording ---
        client.start_recorder(os.path.join(args.output, "recording.log"))

        # --- Action: car drives, cyclist follows ---
        car.set_autopilot(True)
        if cyclist:
            cyclist.set_autopilot(True)

        # Let the scene play
        print(f"Recording {args.duration}s...")
        time.sleep(args.duration)

        # --- Stop ---
        client.stop_recorder()
        camera.stop()
        print(f"Done! {frame_count[0]} frames saved.")
        print(f"Convert: ffmpeg -framerate 30 -i {args.output}/%06d.png -c:v libx264 -pix_fmt yuv420p scene.mp4")

    finally:
        # Cleanup
        for actor in reversed(actors):
            if actor.is_alive:
                actor.destroy()
        print("Actors cleaned up.")


if __name__ == "__main__":
    main()
