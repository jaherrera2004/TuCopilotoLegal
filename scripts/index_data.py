import sys
import os
import json
import glob

# Add the parent directory to sys.path to allow importing services
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from services.chroma_service import ChromaService

def index_articles():
    chroma_service = ChromaService()
    base_path = os.path.join(os.path.dirname(__file__), '..', 'articulos')
    json_files = glob.glob(os.path.join(base_path, '*.json'))

    print(f"Encontrados {len(json_files)} archivos JSON para procesar.")

    for json_file in json_files:
        print(f"Procesando archivo: {json_file}")
        with open(json_file, 'r', encoding='utf-8') as f:
            try:
                articles = json.load(f)
                
                # Verificar si es una lista de artículos
                if isinstance(articles, list):
                    for article in articles:
                        process_article(chroma_service, article)
                else:
                    # Si el JSON es un solo objeto (aunque parece que son listas)
                    process_article(chroma_service, articles)
                    
            except json.JSONDecodeError as e:
                print(f"Error al leer JSON {json_file}: {e}")
            except Exception as e:
                print(f"Error inesperado procesando {json_file}: {e}")

def process_article(chroma_service, article):
    try:
        article_id = str(article.get('numero_articulo', ''))
        if not article_id:
            print("Artículo sin número, saltando...")
            return

        # Verificar si el artículo ya existe
        if chroma_service.article_exists(article_id):
            print(f"Artículo {article_id} ya existe, saltando...")
            return

        title = article.get('titulo_articulo', '')
        summary = article.get('resumen', '')
        keywords = ", ".join(article.get('palabras_clave', []))
        
        # Construir el texto que será vectorizado
        # Incluimos información relevante para la búsqueda semántica
        text_to_embed = f"Artículo {article_id}: {title}\n\nResumen: {summary}\n\nPalabras clave: {keywords}"
        
        # Metadatos útiles para recuperar después
        metadata = {
            "article_id": article_id,
            "title": title,
            "chapter": article.get('capitulo', '')
        }

        print(f"Guardando artículo {article_id}...")
        chroma_service.save_article(article_id, text_to_embed, metadata)
        
    except Exception as e:
        print(f"Error guardando artículo {article.get('numero_articulo')}: {e}")

if __name__ == "__main__":
    index_articles()
