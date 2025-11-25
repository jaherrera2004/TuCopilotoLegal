import chromadb
import os
from services.gemini_service import GeminiService

class ChromaService:
    def __init__(self, host=None, port=None, collection_name="legal_articles"):
        if host is None:
            host = os.getenv("CHROMA_HOST", "localhost")
        if port is None:
            port = int(os.getenv("CHROMA_PORT", 8000))
            
        self.client = chromadb.HttpClient(host=host, port=port)
        self.collection = self.client.get_or_create_collection(name=collection_name)
        self.gemini_service = GeminiService()

    def article_exists(self, article_id):
        """
        Verifica si un artículo ya existe en la colección.
        """
        results = self.collection.get(ids=[article_id])
        return len(results['ids']) > 0

    def save_article(self, article_id, text, metadata=None):
        """
        Guarda un artículo vectorizado en ChromaDB.
        """
        if metadata is None:
            metadata = {}
        
        # Verificar si el artículo ya existe
        if self.article_exists(article_id):
            print(f"Artículo {article_id} ya existe.")
            return
        
        # Generar embedding para el documento usando GeminiService
        embedding = self.gemini_service.get_embedding(text, "RETRIEVAL_DOCUMENT")
        
        # Guardar en ChromaDB
        self.collection.upsert(
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata],
            ids=[article_id]
        )
        print(f"Artículo {article_id} guardado exitosamente.")

    def search_articles(self, query_text, n_results=5):
        """
        Busca artículos relevantes basados en una consulta.
        """
        # Generar embedding para la consulta usando GeminiService
        query_embedding = self.gemini_service.get_embedding(query_text, "RETRIEVAL_QUERY")
        
        # Realizar la búsqueda en ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        return results
