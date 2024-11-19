from flask import Flask, request, jsonify
import os
import requests
from concurrent.futures import ThreadPoolExecutor
from Step1_Framing import split_video_into_scenes
from Step2_Describing import procesar_imagenes_y_guardar_descripciones
from Step2_Transcribing import process_video
from Step3_Tokenizer import procesar_videos_para_tokenizacion
from Step4_Cleaning import generar_json_palabras_clave
from Step5_QueryAI import process_keywords

app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=5)

FRAMES_BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "videos/frames")
VIDEOS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "videos")
TEXT_DIR = os.path.join(VIDEOS_DIR, "TextFromVideo")

os.makedirs(VIDEOS_DIR, exist_ok=True)
os.makedirs(FRAMES_BASE_DIR, exist_ok=True)
os.makedirs(TEXT_DIR, exist_ok=True)

API_URL = "http://localhost:8000/upload"  # URL de la API de destino

def process_video_pipeline(video_path, video_name):
    try:
        frame_paths = split_video_into_scenes(video_path, FRAMES_BASE_DIR)
    except Exception as e:
        return {"status": "error", "message": f"Error in scene splitting: {str(e)}"}

    try:
        procesar_imagenes_y_guardar_descripciones(FRAMES_BASE_DIR)
    except Exception as e:
        return {"status": "error", "message": f"Error in describing images: {str(e)}"}

    try:
        process_video(video_path, "vosk", TEXT_DIR)
    except Exception as e:
        return {"status": "error", "message": f"Error in video transcription: {str(e)}"}

    try:
        description_path = os.path.join(FRAMES_BASE_DIR, "descripciones.txt")
        transcription_path = os.path.join(TEXT_DIR, "transcripcion.txt")
        procesar_videos_para_tokenizacion(video_name, description_path, transcription_path)
    except Exception as e:
        return {"status": "error", "message": f"Error in tokenization: {str(e)}"}

    try:
        keywords_output_path = "videos/video.mp4_palabras_clave.txt"
        json_path = "keyWords.txt"
        generar_json_palabras_clave(keywords_output_path, json_path)
    except Exception as e:
        return {"status": "error", "message": f"Error in JSON generation: {str(e)}"}

    try:
        inputfile = "keyWords.txt"
        outfile = "movie_data.json"
        process_keywords(inputfile,outfile)
    except Exception as e:
        return {"status": "error", "message": f"Error in keyword processing: {str(e)}"}

    # Enviar el archivo JSON y el video a otra API
    try:
        with open(outfile, 'rb') as json_file, open(video_path, 'rb') as video_file:
            files = {
                'json': ('response.json', json_file, 'application/json'),
                'video': (video_name, video_file, 'video/mp4')
            }
            response = requests.post(API_URL, files=files)
            response.raise_for_status()
    except Exception as e:
        return {"status": "error", "message": f"Error sending data to external API: {str(e)}"}

    os.remove(video_path)
    return {"status": "success", "message": "Video processed and sent successfully"}

@app.route('/upload', methods=['POST'])
def upload_and_process_video():
    video = request.files.get('video')
    if not video or not video.filename.endswith('.mp4'):
        return jsonify({"error": "No valid MP4 video file provided"}), 400

    video_path = os.path.join(VIDEOS_DIR, video.filename)
    video.save(video_path)

    future = executor.submit(process_video_pipeline, video_path, video.filename)
    result = future.result()  # Ejecutar la tarea y esperar su finalización

    return jsonify(result), 200 if result["status"] == "success" else 500

if __name__ == "__main__":
    app.run(debug=True)
