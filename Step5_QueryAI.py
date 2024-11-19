import openai
import json
import os

# Configurar la API de OpenAI
API_KEY = "INGRESAR API KEY"
openai.api_key = API_KEY

def read_keywords(file_path):
    """
    Lee las palabras clave desde un archivo de texto.
    
    Args:
        file_path (str): Ruta del archivo de texto a leer.
        
    Returns:
        str: Contenido del archivo como una cadena.
        None: Si el archivo no existe o no puede ser leído.
    """
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return {"error": f"El archivo '{file_path}' no existe."}

def format_json_response(text):
    """
    Intenta extraer y formatear el JSON de la respuesta de la API.
    
    Args:
        text (str): Texto que contiene JSON.
        
    Returns:
        dict: JSON parseado o diccionario de error.
    """
    try:
        # Intentar encontrar el JSON en el texto
        start_idx = text.find('{')
        end_idx = text.rfind('}') + 1
        if start_idx != -1 and end_idx != -1:
            json_str = text[start_idx:end_idx]
            return json.loads(json_str)
        else:
            return {
                "error": "No se encontró JSON válido en la respuesta",
                "raw_response": text
            }
    except json.JSONDecodeError:
        return {
            "error": "Error al decodificar JSON",
            "raw_response": text
        }

def query_openai(prompt, model="gpt-4o"):
    """
    Envía un prompt a la API de OpenAI y obtiene una respuesta JSON.

    Args:
        prompt (str): El texto del prompt para enviar a la API.
        model (str): El modelo a usar, por defecto 'gpt-4'.

    Returns:
        dict: Respuesta formateada como JSON.
    """
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "Debes responder siempre en formato JSON válido, sin texto adicional."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200,
            response_format={ "type": "json_object" }  # Forzar respuesta JSON para modelos que lo soporten
        )
        response_text = response['choices'][0]['message']['content'].strip()
        return format_json_response(response_text)
    except Exception as e:
        return {
            "error": f"Error al consultar la API de OpenAI: {str(e)}",
            "status": "error"
        }

def save_to_json(data, output_path):
    """
    Guarda un diccionario en un archivo JSON, preservando caracteres especiales.
    
    Args:
        data (dict): Datos a guardar.
        output_path (str): Ruta del archivo de salida.
    Returns:
        dict: Estado de la operación en formato JSON.
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
        return {
            "status": "success",
            "message": f"Datos guardados en '{output_path}'."
        }
    except Exception as e:
        return {
            "status": "error",
            "error": f"Error al guardar los datos en JSON: {str(e)}"
        }

def delete_file(file_path):
    """
    Elimina un archivo del sistema.

    Args:
        file_path (str): Ruta del archivo a eliminar.
    Returns:
        dict: Estado de la operación en formato JSON.
    """
    try:
        os.remove(file_path)
        return {
            "status": "success",
            "message": f"Archivo '{file_path}' eliminado."
        }
    except Exception as e:
        return {
            "status": "error",
            "error": f"Error al eliminar el archivo '{file_path}': {str(e)}"
        }

def process_keywords(input_file, output_file):
    """
    Procesa un archivo de palabras clave, consulta la API de OpenAI y guarda la respuesta en JSON.

    Args:
        input_file (str): Ruta del archivo de entrada con palabras clave.
        output_file (str): Ruta del archivo de salida donde se guardará el JSON.
    Returns:
        dict: Resultado del procesamiento en formato JSON.
    """
    
    print("Procesando palabras clave...", input_file)
    
    result = {"status": "processing", "steps": []}
    
    # Leer las palabras clave desde el archivo
    keywords = read_keywords(input_file)
    if isinstance(keywords, dict) and "error" in keywords:
        return {"status": "error", "error": keywords["error"]}
    
    result["steps"].append({"step": "read_keywords", "status": "success"})
    
    # Crear el prompt
    prompt = (
        f"Dado el siguiente texto de palabras clave:\n{keywords}\n"
        "Genera una película que coincida con estas palabras clave y devuélvelo en el siguiente formato JSON:\n"
        "{\n"
        "  'title': '<Movie Title>',\n"
        "  'genre': [<List of Genres>],\n"
        "  'protagonist': '<Description of the protagonist>',\n"
        "  'director': '<Director\\'s Name>'\n"
        "}"
    )
    
    # Consultar a OpenAI
    response_json = query_openai(prompt)
    if "error" in response_json:
        result["status"] = "error"
        result["error"] = response_json["error"]
        return result
    
    result["steps"].append({"step": "api_query", "status": "success"})
    
    # Guardar los resultados
    save_result = save_to_json(response_json, output_file)
    result["steps"].append({"step": "save_json", "status": save_result["status"]})
    
    # Eliminar el archivo original
    delete_result = delete_file(input_file)
    result["steps"].append({"step": "delete_original", "status": delete_result["status"]})
    
    result["status"] = "success"
    result["final_output"] = response_json
    return result

if __name__ == "__main__":
    INPUT_FILE = "keyWords.txt"
    OUTPUT_FILE = "movie_data.json"
    result = process_keywords(INPUT_FILE, OUTPUT_FILE)
    print(json.dumps(result, indent=2, ensure_ascii=False))