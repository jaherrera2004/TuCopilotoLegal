import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        genai.configure(api_key=self.api_key)

    def get_model(self, model_name="gemini-2.5-flash"):
        return genai.GenerativeModel(model_name)

    def get_embedding(self, text, task_type):
        """
        Genera embeddings usando el modelo gemini-embedding-001.
        task_type puede ser 'RETRIEVAL_DOCUMENT' o 'RETRIEVAL_QUERY'.
        """
        result = genai.embed_content(
            model="models/gemini-embedding-001",
            content=text,
            task_type=task_type
        )
        return result['embedding']

    def generate_response(self, prompt, model_name="gemini-2.5-flash"):
        model = self.get_model(model_name)
        response = model.generate_content(prompt)
        return response.text
