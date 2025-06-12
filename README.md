# Ingestor-IoT

Este proyecto levanta un servicio Python que consume mensajes MQTT y los guarda en una base de datos PostgreSQL/TimescaleDB.

---

## Requisitos

- Docker & Docker Compose  
- VS Code + [Remote – Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)  
- Un archivo `.env` en la raíz con tus variables de entorno:
  ```dotenv
  DB_HOST=...
  DB_NAME=...
  DB_USER=...
  DB_PASS=...
  MQTT_BROKER=broker
  MQTT_PORT=8883
  MQTT_TOPIC=sensors/+/temperature
  CA_CERT_PATH=/certs/ca.crt
  ```

---

## Usar el Dev Container (VS Code)

1. Abre la paleta de comandos (`⇧⌘P` / `Ctrl+Shift+P`).  
2. Ejecuta **Remote-Containers: Reopen Folder in Container**.  
3. VS Code construirá el contenedor usando `.devcontainer/devcontainer.json` y te abrirá un shell en `/workspace`.  
4. Abre un terminal integrado (**Terminal > New Terminal**) y lanza tu script:
   ```fish
   python app2.py
   ```

---

## Construir y ejecutar sin Docker Compose

Desde la raíz del proyecto:

```fish
# 1) Build de la imagen
docker build \
  -f .devcontainer/Dockerfile \
  -t ingestor-iot:latest \
  .

# 2) Run pasándole el .env y exponiendo el puerto 5000
docker run --rm -it \
  --env-file .env \
  -p 5000:5000 \
  ingestor-iot:latest
```

---

## Usar con Docker Compose

1. Crea un archivo `docker-compose.yml` en la raíz:

   ```yaml
   version: '3.8'
   services:
     ingestor-iot:
       build:
         context: .
         dockerfile: .devcontainer/Dockerfile
       image: ingestor-iot:latest
       env_file:
         - .env
       ports:
         - "5000:5000"
   ```

2. Ejecuta:
   ```fish
   docker-compose up --build
   ```

---

## Limpieza

Para eliminar imágenes y contenedores huérfanos:

```fish
docker system prune --volumes
```
