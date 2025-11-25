import os
from flask import Flask, render_template
from dotenv import load_dotenv
from services.chroma_service import ChromaService
from scripts.index_data import index_articles
from controllers.chat_controller import chat_bp

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
app.register_blueprint(chat_bp)

# Inicializar ChromaService
chroma_service = ChromaService()

@app.route('/')
def index():
    # Obtener información de la colección usando el servicio
    count = chroma_service.collection.count()
    return render_template('index.html', count=count)

if __name__ == '__main__':
    # Ejecutar la indexación de artículos al iniciar la app
    print("Iniciando indexación de artículos...")
    index_articles()
    print("Indexación completada.")
    
    app.run(host='0.0.0.0', debug=True)
