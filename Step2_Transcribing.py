import os
import requests
from pydub import AudioSegment
from vosk import Model, KaldiRecognizer
import json
import spacy
import tempfile

# Cargar el modelo de Spacy
nlp = spacy.load("es_core_news_sm")  # Asegúrate de tener este modelo de spaCy descargado

def extract_audio_from_video(video_path, audio_output_path="audio.wav"):
    """
    Extrae el audio del video y lo guarda como un archivo .wav
    """
    audio = AudioSegment.from_file(video_path)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(audio_output_path, format="wav")
    return audio_output_path

def transcribe_audio_with_vosk(audio_path, model_path="model"):
    """
    Transcribe el audio utilizando el modelo Vosk
    """
    if not os.path.exists(model_path):
        print("Modelo de Vosk no encontrado. Descarga el modelo y colócalo en el directorio especificado.")
        return

    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)
    transcript = []

    with open(audio_path, "rb") as audio_file:
        while True:
            data = audio_file.read(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                transcript.append(result.get("text", ""))

        result = json.loads(recognizer.FinalResult())
        transcript.append(result.get("text", ""))

    return " ".join(transcript)

def generate_video_description(video_path):
    """
    Genera una descripción del video utilizando el modelo de spaCy.
    """
    # Aquí se utilizará spaCy para analizar y generar la descripción
    doc = nlp(video_path)  # Se utiliza spaCy para procesar el contenido textual (asegurarte de tener algún texto para esto)
    description = " ".join([sent.text for sent in doc.sents])  # Crear una descripción básica de las oraciones
    return description

def process_video(video_path, model_path, output_dir):
    """
    Procesa un video, extrayendo audio, transcribiéndolo y generando una descripción.
    """
    # Extraer audio del video
    audio_path = extract_audio_from_video(video_path)
    
    # Transcribir el audio con Vosk
    transcription = transcribe_audio_with_vosk(audio_path, model_path)
    
    # Guardar la transcripción en el directorio TextFromVideo
    transcription_file_path = os.path.join(output_dir, "transcripcion.txt")
    with open(transcription_file_path, 'w', encoding='utf-8') as f:
        f.write(transcription)
    print(f"Transcripción guardada en {transcription_file_path}")
    
    # Generar una descripción del video
    description = generate_video_description(video_path)
    
    # Guardar la descripción
    description_file_path = os.path.join(output_dir, "descripcion.txt")
    with open(description_file_path, 'w', encoding='utf-8') as f:
        f.write(description)
    print(f"Descripción guardada en {description_file_path}")

    # Limpiar los archivos temporales
    os.remove(audio_path)
    print(f"Archivo de audio temporal eliminado.")

# Ejecutar el proceso para el video especificado
if __name__ == "__main__":
    video_path = "Videos/video.mp4"  # Ruta de tu video en la carpeta Videos
    model_path = "D:/TESIS/FlujoCompleto/vosk"  # Ruta de tu modelo de Vosk
    output_dir = "Videos/TextFromVideo"  # Ruta donde se guardarán la transcripción y la descripción
    os.makedirs(output_dir, exist_ok=True)
    
    process_video(video_path, model_path, output_dir)
