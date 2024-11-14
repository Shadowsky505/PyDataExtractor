import os
import spacy
from translate import Translator

# Cargar el modelo de spaCy en inglés
nlp = spacy.load("en_core_web_sm")

def traducir_a_ingles(texto):
    """Traduce un texto al inglés usando la librería translate."""
    traductor = Translator(to_lang="en")
    try:
        texto_traducido = traductor.translate(texto)
    except Exception as e:
        print(f"Error en la traducción: {e}")
        texto_traducido = texto  # Si hay error, usar el texto original
    return texto_traducido

def extraer_palabras_clave(texto):
    """Extrae palabras clave (sustantivos, nombres propios, verbos, adjetivos) de un texto en inglés."""
    doc = nlp(texto)
    palabras_clave = [token.lemma_ for token in doc if token.pos_ in ["NOUN", "PROPN", "VERB", "ADJ"] and not token.is_stop]
    return palabras_clave

def procesar_videos_para_tokenizacion(video_name, descripcion_path, transcripcion_path, output_dir="videos"):
    os.makedirs(output_dir, exist_ok=True)
    output_file_path = os.path.join(output_dir, f"{video_name}_palabras_clave.txt")
    
    # Leer descripciones y transcripción
    with open(descripcion_path, 'r', encoding='utf-8') as f:
        descripciones_texto = f.read()
    with open(transcripcion_path, 'r', encoding='utf-8') as f:
        transcripcion_texto = f.read()
    
    # Traducir descripciones y transcripción al inglés
    texto_completo = descripciones_texto + " " + transcripcion_texto
    texto_traducido = traducir_a_ingles(texto_completo)
    
    # Extraer palabras clave
    palabras_clave = extraer_palabras_clave(texto_traducido)
    
    # Guardar palabras clave en archivo
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(", ".join(palabras_clave))
    
    print(f"Palabras clave guardadas en {output_file_path}")
    return output_file_path

# Ejemplo de uso:
# procesar_videos_para_tokenizacion("Video1","videos/frames/tex1.txt","videos/TextFromVideo/descripciones.txt")
