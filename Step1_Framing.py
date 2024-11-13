import os
import subprocess
from scenedetect import open_video, SceneManager
from scenedetect.detectors import ContentDetector

def split_video_into_scenes(video_path, base_dir="Videos/Frames", threshold=27.0):
    output_dir = os.path.join(base_dir)  # Carpeta específica dentro de Frames
    os.makedirs(output_dir, exist_ok=True)
    
    video = open_video(video_path)
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=threshold))
    
    scene_manager.detect_scenes(video, show_progress=True)
    scene_list = scene_manager.get_scene_list()
    
    frame_paths = []
    for idx, (start_time, end_time) in enumerate(scene_list):
        frame_output_path = os.path.join(output_dir, f"frame_scene_{idx+1}.jpg")
        
        subprocess.run([
            "ffmpeg", "-i", video_path, "-vf",
            f"select='gte(t,{start_time.get_seconds()})'", "-vframes", "1",
            "-q:v", "2", frame_output_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print(f"Fotograma guardado en: {frame_output_path}")
        frame_paths.append(frame_output_path)
    
    print(f"Todos los fotogramas se encuentran en: {output_dir}")
    return frame_paths
