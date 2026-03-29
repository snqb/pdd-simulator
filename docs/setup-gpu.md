# GPU Setup для CARLA

## Проблема

Мы на macOS ARM (M2 Pro). CARLA = UE5.5 = нужен x86_64 Linux + NVIDIA GPU.

## Варианты

### 1. Vast.ai (рекомендую — дёшево)
```bash
pip install vastai
vastai set api-key YOUR_KEY

# Найти машину с RTX 4090, Ubuntu
vastai search offers 'gpu_name=RTX_4090 num_gpus=1 dph<0.50 inet_down>200'

# Арендовать
vastai create instance INSTANCE_ID --image carlasim/carla:0.10.0 --disk 50
```
~$0.30–0.50/час за RTX 4090

### 2. RunPod
```bash
pip install runpodctl
runpodctl config --apiKey YOUR_KEY
# Community Cloud RTX 4090 ~$0.40/hr
```

### 3. Своя машина
Любой десктоп/ноут с NVIDIA GPU (GTX 1070+ / RTX 3060+), Linux.
```bash
docker pull carlasim/carla:0.10.0
docker run --privileged --gpus all -p 2000:2000 -p 2001:2001 carlasim/carla:0.10.0
```

### 4. Coolify (если есть сервер с GPU)
Deploy CARLA как Docker сервис.

## Подключение с мака

```bash
# Python клиент (работает на маке)
pip install carla==0.10.0

# Подключение к удалённому серверу
python3 -c "
import carla
client = carla.Client('GPU_SERVER_IP', 2000)
print(client.get_server_version())
"
```

## Просмотр удалённо

### VNC (самый простой)
На GPU-сервере:
```bash
apt install -y tigervnc-standalone-server
vncserver :1 -geometry 1920x1080
```
На маке: Screen Sharing → `vnc://GPU_SERVER_IP:5901`

### Parsec (лучше latency)
Установить Parsec на сервер и мак.

### Web-стрим камеры (headless)
CARLA может работать в `-RenderOffScreen` режиме.
Камера → кадры → WebSocket → браузер на маке.
