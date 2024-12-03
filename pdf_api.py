from flask import Flask, request, jsonify
import fitz  # PyMuPDF
import os
import re

app = Flask(__name__)

def extract_text_from_pdf(pdf_path):
    """
    Extrae el texto de un archivo PDF.
    
    Args:
    pdf_path (str): Ruta del archivo PDF.
    
    Returns:
    str: Texto extraído.
    """
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            # Extraer texto de la página
            text += page.get_text("text")
            
            # Extraer tablas de la página
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" in block:
                    table_text = "\n\n| "
                    for line in block["lines"]:
                        table_text += " | ".join([span["text"] for span in line["spans"]]) + " |\n"
                    text += table_text
        
        print(f"Texto extraído de {pdf_path}")
        return text
    
    except Exception as e:
        print(f"Error al procesar {pdf_path}: {e}")
        return ""

def clean_text(text):
    """
    Limpia el texto eliminando guiones con saltos de línea, saltos de línea seguidos por una letra minúscula,
    dobles espacios y espacios seguidos de un salto de línea.
    
    Args:
    text (str): Texto a limpiar.
    
    Returns:
    str: Texto limpio.
    """
    text = re.sub(r'-\n', '', text)
    text = re.sub(r'\n(?=[a-z])', ' ', text)
    text = re.sub(r'\. *\n+', '.\n', text)
    text = re.sub(r' +', ' ', text)
    text = re.sub(r' \n', ' ', text)

    return text

@app.route('/extract-text', methods=['POST'])
def extract_text():
    """
    Endpoint para extraer texto de un archivo PDF enviado.
    
    Returns:
    JSON: Texto extraído y limpio del archivo PDF.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No se encontró el archivo PDF"}), 400

    pdf_file = request.files['file']
    
    # Guardar temporalmente el archivo
    pdf_path = os.path.join("temp", pdf_file.filename)
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    pdf_file.save(pdf_path)

    # Extraer y limpiar el texto
    extracted_text = extract_text_from_pdf(pdf_path)
    cleaned_text = clean_text(extracted_text)

    # Eliminar el archivo temporal
    os.remove(pdf_path)

    return jsonify({"text": cleaned_text})

if __name__ == "__main__":
    app.run(debug=True)
