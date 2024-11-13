# client.py
import requests

# URL del servidor donde está corriendo la API
url = 'http://127.0.0.1:5000/upload'
video_path = 'video.mp4'

with open(video_path, 'rb') as video_file:
    files = {'video': video_file}
    response = requests.post(url, files=files)

print(response.json())
