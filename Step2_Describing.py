# Step2_Describing.py
import os
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

def procesar_imagenes_y_guardar_descripciones(ruta_frames, extensiones_imagenes={'.jpg'}):
    """
    Procesa imágenes en las subcarpetas de 'ruta_frames' y genera descripciones para cada una.
    
    Parameters:
    - ruta_frames: Ruta al directorio principal de fotogramas de los videos.
    - extensiones_imagenes: Extensiones de archivos de imagen permitidas (por defecto .jpg).
    
    """
    # Cargar el modelo BLIP para generación de descripciones
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    
   
    descripciones = []
    
    for archivo in os.listdir(ruta_frames):
        if os.path.splitext(archivo)[1].lower() in extensiones_imagenes:
            ruta_imagen = os.path.join(ruta_frames, archivo)
            
            # Procesamos la imagen para generar la descripción
            image = Image.open(ruta_imagen).convert('RGB')
            inputs = processor(image, return_tensors="pt")
            output = model.generate(**inputs)
            
            # Decodificamos la descripción generada y almacenamos
            description = processor.decode(output[0], skip_special_tokens=True)
            descripciones.append(description)
            
            # Eliminamos la imagen procesada
            os.remove(ruta_imagen)
            print(f"Imagen {archivo} procesada y eliminada.")
    
    # Guardamos las descripciones en un archivo de texto
    texto_final = " ".join(descripciones)
    ruta_txt = os.path.join(ruta_frames, "descripciones.txt")
    with open(ruta_txt, 'w') as f:
        f.write(texto_final)
    print(f"Descripciones guardadas en {ruta_txt}")
    
    print("Proceso completado: todas las imágenes han sido procesadas y las descripciones guardadas.")
