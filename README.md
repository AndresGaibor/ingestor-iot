# Ingestor-IoT

Este proyecto levanta un servicio Python que consume mensajes MQTT y los guarda en una base de datos PostgreSQL/TimescaleDB.

---

## Requisitos

- Docker & Docker Compose  
- VS Code + [Remote – Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)  
- Un archivo `.env` en la raíz con tus variables de entorno:
  ```dotenv
  DB_HOST=localhost
  DB_NAME=iotdb
  DB_USER=iotuser
  DB_PASS=iotpass
  MQTT_BROKER=broker
  MQTT_PORT=8883
  MQTT_TOPIC=sensors/+/temperature
  ```
  **Nota**: El fichero `certs/ca.crt` debe contener el certificado de la CA que firma tu broker MQTT. No se incluye en el repositorio; descárgalo de tu proveedor o administrador y colócalo en la carpeta `certs/` en la raíz del proyecto.

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

1. Crear las carpetas donde se guardaran los volumenes de los contenedores
	- data/timescale
	- data/grafana
	- certs/ca.crt

2. Crea (o edita) un archivo `docker-compose.yml` en la raíz:
```bash
docker compose up -d
```

## Usar el servicio MQTT o TIMESCALE desde una maquina remota
	1. [Descargar e instalar cloudflared](https://github.com/cloudflare/cloudflared/releases)
	2. Conectarse al servicio
	```bash
		cloudflared access tcp --hostname (subdominio).dominio.com --url localhost:8833
	```

De esta forma podremos lanzar peticiones tcp a **localhost:8833**

Para mas inforformacion de cloudflared, revistar esta guia: [Como usar cloudflared para exponer puertos](https://smoggy-stallion-237.notion.site/conectar-SQL-Server-con-VSC-12c09af24d13437da5b5159c51626cdd)

