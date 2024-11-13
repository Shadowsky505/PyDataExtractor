# mainAPI.py
from flask import Flask, request, jsonify
import os
import threading
from datetime import datetime
from Step1_Framing import split_video_into_scenes
from Step2_Describing import procesar_imagenes_y_guardar_descripciones
from Step2_Transcribing import transcribe_audio_with_vosk
from Step3_Tokenizer import procesar_videos_para_tokenizacion

app = Flask(__name__)

# Directorio base para guardar los fotogramas y los videos
FRAMES_BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "videos/frames")
VIDEOS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "videos")

os.makedirs(VIDEOS_DIR, exist_ok=True)

def describe_images(frames_dir):
    procesar_imagenes_y_guardar_descripciones(frames_dir)

def transcribe_audio(video_path, frames_dir):
    transcribe_audio_with_vosk(video_path, frames_dir)

@app.route('/upload', methods=['POST'])
def upload_and_process_video():
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video = request.files['video']
    
    if video.filename.endswith('.mp4'):
        # Guardamos el video en la carpeta "videos" dentro del directorio de trabajo
        temp_video_path = os.path.join(VIDEOS_DIR, video.filename)
        video.save(temp_video_path)
        
        print("DIRECTORIOS CREADOS POR MAIN")
        # Crear un subdirectorio único dentro de "frames" para guardar los fotogramas de este video
        video_frames_dir = os.path.join(FRAMES_BASE_DIR)
        os.makedirs(video_frames_dir, exist_ok=True)
        
        
        print("DIRECTORIO CREADO POR STEP1")
        # Procesamos el video para dividirlo en escenas y guardar los fotogramas en el nuevo directorio
        frame_paths = split_video_into_scenes(temp_video_path, video_frames_dir)
        
        # Ejecutar Describing y Transcribing en paralelo
        describe_images("videos/frames")
        transcribe_audio(temp_video_path,"videos/TextFromVideo")
        
        
        # Ejecutar el paso de tokenización de palabras clave
        # procesar_videos_para_tokenizacion(video_frames_dir)
        
        # Limpiar la carpeta de video después de procesarlo
        os.remove(temp_video_path)

        return jsonify({
            "message": "Video processed successfully",
        #    "frames": frame_paths
        }), 200
    else:
        return jsonify({"error": "File must be an MP4 video"}), 400

if __name__ == "__main__":
    app.run(debug=True)
