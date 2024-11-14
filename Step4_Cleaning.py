import os
import json

def leer_archivo(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as file:
        return file.read()

def depurar_palabras_clave(palabras_clave):
    return list(set(palabras_clave))

def generar_json_palabras_clave(ruta_palabras_clave, ruta_json_general):
    # Lee el archivo de palabras clave dentro de Videos
    if not os.path.exists(ruta_palabras_clave):
        print(f"El archivo {ruta_palabras_clave} no existe.")
        return
    
    palabras_clave_texto = leer_archivo(ruta_palabras_clave)
    palabras_clave = palabras_clave_texto.split(", ")
    
    # Depura y guarda las palabras clave en la estructura de JSON deseada
    datos_json_general = {
        "tags": depurar_palabras_clave(palabras_clave)
    }
    
    with open(ruta_json_general, 'w', encoding='utf-8') as json_file:
        json.dump(datos_json_general, json_file, ensure_ascii=False, indent=4)
    
    print(f"Archivo JSON general creado en {ruta_json_general}")

# Ejemplo de uso
# ruta_palabras_clave = 'videos/palabras.txt'  # Ubicación del archivo dentro de Videos
# ruta_json_general = 'palabras_clave_general.json'  # Ruta de salida del JSON
# generar_json_palabras_clave(ruta_palabras_clave, ruta_json_general)
