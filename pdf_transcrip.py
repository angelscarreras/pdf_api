import fitz  # PyMuPDF
import os
import re

def extract_text_from_pdf (pdf_path):
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
    # Reemplazar guiones seguidos de saltos de línea por una cadena vacía para recomponer palabras cortadas
    text = re.sub(r'-\n', '', text)
    
    # Reemplazar saltos de línea seguidos de una letra minúscula por un espacio para mantener la continuidad de las frases
    text = re.sub(r'\n(?=[a-z])', ' ', text)
    
    # Reemplazar saltos de línea múltiples por un único salto de línea si están precedidos por un punto
    text = re.sub(r'\. *\n+', '.\n', text)
    
    # Reemplazar dobles espacios por un solo espacio
    text = re.sub(r' +', ' ', text)

    # Reemplazar espacio seguido de salto de línea por un solo espacio
    text = re.sub(r' \n', ' ', text)

    return text

def process_files(paths):
    """
    Procesa una lista de tuplas de rutas de documentos PDF y archivos de texto de salida.
    
    Args:
    paths (list of tuples): Lista de tuplas con la ruta del PDF y la ruta del archivo de texto de salida.
                            [(pdf_path1, output_txt_path1), (pdf_path2, output_txt_path2), ...]
    """
    for pdf_path, output_txt_path in paths:
        text = extract_text_from_pdf(pdf_path)
        if text:
            cleaned_text = clean_text(text)
            
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(output_txt_path), exist_ok=True)
            
            with open(output_txt_path, "w", encoding="utf-8") as f:
                f.write(cleaned_text)
            
            print(f"Texto limpio guardado en {output_txt_path}")

if __name__ == "__main__":
    # Lista de rutas de documentos PDF y archivos de texto de salida como tuplas
    paths = [
       ("/Users/belencarreras/gastos_/text/gpt_huesped_asc.pdf", "text/limpio_gpt_huesped_asc.md")
    ]
    
    process_files(paths)
