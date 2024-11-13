import os
import json
import requests

api_url = "http://127.0.0.1:5000/api/movies"

ruta_principal = 'frames'

ruta_json_general = 'palabras_clave_general.json'

def leer_archivo(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as file:
        return file.read()

def depurar_palabras_clave(palabras_clave):
    return list(set(palabras_clave))  # Eliminar duplicados convirtiendo a conjunto y luego a lista

response = requests.get(api_url)
if response.status_code != 200:
    raise Exception("Error al consultar la API")

datos_api = response.json()

datos_json_general = []

for subcarpeta in os.listdir(ruta_principal):
    ruta_subcarpeta = os.path.join(ruta_principal, subcarpeta)
    
    if os.path.isdir(ruta_subcarpeta):
        video_data = next((item for item in datos_api if item["ID"] == subcarpeta), None)
        
        if video_data:
            usuario_id = video_data["IDUsuario"]
            
            ruta_palabras_clave = os.path.join(ruta_subcarpeta, "palabras_clave.txt")
            
            if os.path.exists(ruta_palabras_clave):
                palabras_clave_texto = leer_archivo(ruta_palabras_clave)
                palabras_clave = palabras_clave_texto.split(", ")
                
                palabras_clave_depuradas = depurar_palabras_clave(palabras_clave)
                
                datos_json_general.append({
                    "IDVideo": subcarpeta,  # Usamos el nombre de la subcarpeta como ID del video
                    "IDUsuario": usuario_id,
                    "PalabrasClave": palabras_clave_depuradas
                })

with open(ruta_json_general, 'w', encoding='utf-8') as json_file:
    json.dump(datos_json_general, json_file, ensure_ascii=False, indent=4)

print(f"Archivo JSON general creado en {ruta_json_general}")
