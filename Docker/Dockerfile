# Imagen base con soporte para Python y git
FROM python:3.10-slim

# Instalar herramientas necesarias
RUN apt-get update && apt-get install -y --no-install-recommends git wget unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Clonar el repositorio en el contenedor
RUN git clone https://github.com/Shadowsky505/PyDataExtractor.git /app

# Establecer el directorio de trabajo al repositorio clonado
WORKDIR /app

COPY Requirements.txt /app/requirements.txt
# Descargar el modelo de Vosk en la carpeta app como "Vosk.zip"
 RUN wget -O Vosk.zip https://alphacephei.com/vosk/models/vosk-model-fr-0.6-linto-2.2.0.zip \
    && unzip Vosk.zip -d ./vosk \
    && rm Vosk.zip

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Descargar otros recursos necesarios cuando se ejecute el código
# (El script download_model.py manejará esto)
RUN python download_model.py

# Configurar el comando para ejecutar la aplicación
CMD ["python", "app.py"]