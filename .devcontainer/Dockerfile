# Usa una imagen ligera de Python
FROM python:3.11-slim

# Instala dependencias para psycopg2 y SSL
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      gcc \
      libpq-dev \
      ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Crea y sitúa el directorio de trabajo
WORKDIR /workspace

# Copia solo requirements para aprovechar cache de Docker
COPY requirements.txt .

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación
COPY . .

# Expone el puerto de tu aplicación
EXPOSE 5000

# Comando por defecto al abrir contenedor
CMD ["python", "app2.py"]