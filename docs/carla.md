# CARLA для ПДД-контента

## Что это

Open-source симулятор трафика на UE5.5. MIT лицензия. 13.8K ⭐ GitHub.
Создан для autonomous driving, но идеален для образовательного ПДД-контента.

**Версия:** 0.10.0 (декабрь 2024) — UE5.5, Nanite, Lumen.
**Repo:** https://github.com/carla-simulator/carla
**Docs UE5:** https://carla-ue5.readthedocs.io/

## Что есть из коробки

### Готовые карты
- Town01–Town15 — разные типы городов
- **Town10** — красивый, подходит для общих ПДД-сцен
- Каждая карта: дороги, перекрёстки, светофоры, знаки, разметка

### Готовые актёры
- **Машины**: ~50 моделей (седаны, грузовики, мотоциклы, велосипеды)
- **Пешеходы**: ~30 моделей с AI-контроллером (ходят, пересекают дорогу)
- **Велосипедисты**: есть
- **Светофоры**: полный цикл, управляемые через API

### Камеры и сенсоры
- RGB камера (любой ракурс, любое разрешение)
- Depth / Semantic Segmentation камеры
- Bird's eye view (вид сверху — как на твоём фото)

### Погода и освещение
- Время суток (рассвет, полдень, закат, ночь)
- Дождь, туман, мокрая дорога
- Настраивается через API в реальном времени

## Установка

### Вариант 1: Docker (рекомендую)
```bash
# На Linux машине с NVIDIA GPU
docker pull carlasim/carla:0.10.0
docker run --privileged --gpus all --net=host \
  -e DISPLAY=$DISPLAY carlasim/carla:0.10.0
```

### Вариант 2: Бинарник
```bash
# Скачать с GitHub Releases
wget https://carla-releases.s3.us-east-005.backblazeb2.com/Linux/CARLA_0.10.0.tar.gz
tar -xzf CARLA_0.10.0.tar.gz
cd CARLA_0.10.0
./CarlaUnreal.sh
```

### Python клиент (на любой машине)
```bash
pip install carla==0.10.0
```

## Порты

| Порт | Назначение |
|---|---|
| **2000** | RPC (Python API) |
| **2001** | Streaming (сенсоры) |
| **8080** | HTTP (если включить) |

Клиент подключается к `host:2000` — можно удалённо.

## Базовый сценарий

```python
#!/usr/bin/env python3
"""ПДД: Зелёный свет — машина проезжает, пешеход ждёт."""
import carla
import time

# 1. Подключение
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)
world = client.load_world('Town10')

# 2. Настройка погоды
weather = carla.WeatherParameters.ClearNoon
world.set_weather(weather)

# 3. Спавн машины
bp_lib = world.get_blueprint_library()
car_bp = bp_lib.find('vehicle.lincoln.mkz_2020')
spawn_point = world.get_map().get_spawn_points()[0]
car = world.spawn_actor(car_bp, spawn_point)

# 4. Спавн пешехода
walker_bp = bp_lib.find('walker.pedestrian.0001')
walker_spawn = carla.Transform(carla.Location(x=10, y=5, z=1))
walker = world.spawn_actor(walker_bp, walker_spawn)

# 5. Камера сверху (bird's eye)
cam_bp = bp_lib.find('sensor.camera.rgb')
cam_bp.set_attribute('image_size_x', '1920')
cam_bp.set_attribute('image_size_y', '1080')
cam_transform = carla.Transform(
    carla.Location(x=spawn_point.location.x, y=spawn_point.location.y, z=30),
    carla.Rotation(pitch=-90)  # смотрит вниз
)
camera = world.spawn_actor(cam_bp, cam_transform)

# Запись кадров
camera.listen(lambda img: img.save_to_disk(f'output/{img.frame:06d}.png'))

# 6. Машина едет
car.set_autopilot(True)

# 7. Ждём 10 секунд → стоп
time.sleep(10)

# 8. Cleanup
camera.stop()
car.destroy()
walker.destroy()
print("Сцена записана в output/")
```

## ScenarioRunner — Готовые ПДД-паттерны

**Repo:** https://github.com/carla-simulator/scenario_runner (649 ⭐)

Уже реализованные сценарии (из NHTSA типологии аварий):
1. **Пересечение перекрёстка** на зелёный/красный
2. **Пешеход на зебре** — машина должна уступить
3. **Обгон** — встречка
4. **Следование за автомобилем** — соблюдение дистанции
5. **Перестроение** — слепая зона
6. **Экстренное торможение** впереди идущего
7. **Поворот налево** — пропуск встречного потока
8. **Выезд со двора** — ограниченная видимость
9. **Велосипедист** на проезжей части
10. **Проезд кольца**

Каждый сценарий = XML/Python файл. Можно модифицировать параметры.

## Кастомизация

### Добавить свою машину
1. 3D модель в FBX (Blender → Export)
2. Import в UE Editor как Skeletal Mesh
3. Настроить физику (колёса, масса, центр тяжести)
4. Зарегистрировать в CARLA blueprint library
5. Доступна через API: `bp_lib.find('vehicle.custom.my_car')`

### Добавить здание
1. 3D модель в FBX
2. Import в UE Editor → Static Mesh
3. Разместить на карте в UE Editor
4. Re-cook карту

### Создать свою карту
- **RoadRunner** (Mathworks) — визуальный редактор дорог → экспорт в OpenDRIVE → CARLA import
- **OpenStreetMap** → конвертация в OpenDRIVE → CARLA
- **UE Editor** напрямую — ручное размещение

### Что НЕ надо кастомить для ПДД
- Правила движения универсальны — Town10 подходит
- Светофоры, знаки, разметка — всё есть
- Машины/пешеходы — достаточно встроенных

## Запись видео

```python
# Встроенный рекордер — записывает всю симуляцию
client.start_recorder("pdd_scenario_01.log")
# ... прогоняем сценарий ...
client.stop_recorder()

# Воспроизведение с любой камерой
client.replay_file("pdd_scenario_01.log", start=0, duration=30)
```

Или просто: камера → `save_to_disk()` → `ffmpeg -framerate 30 -i output/%06d.png -c:v libx264 video.mp4`

## Удалённый доступ (для macOS)

```bash
# На GPU-сервере: запускаем CARLA
./CarlaUnreal.sh -RenderOffScreen -carla-rpc-port=2000

# На маке: подключаемся
import carla
client = carla.Client('gpu-server-ip', 2000)
```

Для просмотра в реальном времени с мака:
- **VNC/Parsec/Moonlight** к GPU-серверу
- Или стримить камеру через WebSocket (есть примеры)
