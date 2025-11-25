# 🚨 Copiloto Legal - Asistente de Retenes

Sistema de asistencia legal basado en RAG (Retrieval-Augmented Generation) especializado en el Código Nacional de Tránsito de Colombia. Proporciona respuestas precisas y fundamentadas con citas legales verificables.

## 📋 Descripción

Copiloto Legal es un chatbot inteligente que combina búsqueda semántica vectorial con IA generativa para ofrecer asesoría legal sobre normas de tránsito, procedimientos en retenes, multas y derechos del conductor.

### Características principales

- ✅ **RAG (Retrieval-Augmented Generation)**: Búsqueda semántica + IA generativa
- ✅ **Grounding**: Respuestas fundamentadas exclusivamente en documentos legales
- ✅ **Citación automática**: Todas las respuestas incluyen fuentes verificables
- ✅ **Base vectorial**: ChromaDB para búsqueda semántica eficiente
- ✅ **IA avanzada**: Google Gemini (gemini-embedding-001 y gemini-2.5-flash)
- ✅ **Interfaz moderna**: UI responsive con Tailwind CSS
- ✅ **Dockerizado**: Despliegue simple con Docker Compose

## 🏗️ Arquitectura

```
┌─────────────────┐
│   Usuario       │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│   Frontend (HTML/Tailwind/JS)      │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│   Flask App (app.py)                │
│   ├── ChatController                │
│   ├── ChatService                   │
│   ├── ChromaService                 │
│   └── GeminiService                 │
└────┬───────────────────────┬────────┘
     │                       │
     ▼                       ▼
┌─────────────┐      ┌──────────────┐
│  ChromaDB   │      │  Gemini API  │
│  (Vector)   │      │  (Google)    │
└─────────────┘      └──────────────┘
```

## 🚀 Instalación y Despliegue

### Prerrequisitos

- Docker & Docker Compose
- Cuenta de Google Cloud con API Key de Gemini

### Paso 1: Clonar el repositorio

```bash
git clone <repository-url>
cd code
```

### Paso 2: Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
GEMINI_API_KEY=tu_api_key_de_google_gemini
CHROMA_HOST=chromadb
CHROMA_PORT=8000
```

### Paso 3: Ejecutar con Docker Compose

```bash
docker compose up --build
```

Esto iniciará:
- **ChromaDB** en `http://localhost:8000`
- **Flask App** en `http://localhost:5000`

### Paso 4: Acceder a la aplicación

Abre tu navegador en: **http://localhost:5000**

## 📁 Estructura del Proyecto

```
code/
├── app.py                      # Aplicación Flask principal
├── docker-compose.yml          # Configuración Docker
├── Dockerfile                  # Imagen Docker de la app
├── requirements.txt            # Dependencias Python
├── .env                        # Variables de entorno (no incluido en repo)
├── articulos/                  # Documentos legales en JSON
│   ├── 1-30.json
│   ├── 31-60.json
│   └── ...
├── controllers/
│   └── chat_controller.py      # Endpoint /chat
├── services/
│   ├── chat_service.py         # Lógica de negocio del chat
│   ├── chroma_service.py       # Servicio de búsqueda vectorial
│   └── gemini_service.py       # Integración con Gemini API
├── scripts/
│   └── index_data.py           # Script de indexación de artículos
└── templates/
    └── index.html              # Frontend del chat
```

## 🔧 Componentes Principales

### 1. ChromaService (`services/chroma_service.py`)
- Conexión con ChromaDB (puerto 8000)
- Guarda artículos vectorizados usando embeddings de Gemini
- Búsqueda semántica con `RETRIEVAL_QUERY`

### 2. GeminiService (`services/gemini_service.py`)
- Genera embeddings con `gemini-embedding-001`
- Genera respuestas con `gemini-2.5-flash`
- Maneja la configuración de la API

### 3. ChatService (`services/chat_service.py`)
- Coordina la búsqueda vectorial y generación de respuesta
- Construye prompts con instrucciones del sistema
- Aplica técnica de Grounding para fundamentar respuestas

### 4. ChatController (`controllers/chat_controller.py`)
- Endpoint POST `/chat`
- Recibe mensajes del usuario y devuelve respuestas + fuentes

## 📊 Flujo de Datos

1. **Usuario envía pregunta** → Frontend (JavaScript)
2. **POST /chat** → ChatController
3. **Búsqueda semántica** → ChromaService busca los 3 artículos más relevantes
4. **Construcción de prompt** → ChatService incluye contexto legal + pregunta
5. **Generación de respuesta** → GeminiService procesa con IA
6. **Respuesta + fuentes** → Se devuelve al usuario con citas legales

## 🎨 Frontend

La interfaz utiliza:
- **Tailwind CSS** para diseño responsive y moderno
- **Font Awesome** para iconografía
- **Vanilla JavaScript** para manejo de eventos y fetch API
- Animaciones suaves y UX optimizada

## 📝 API Endpoint

### POST `/chat`

**Request:**
```json
{
  "message": "¿Cuál es la multa por no llevar el equipo de carretera?"
}
```

**Response:**
```json
{
  "response": "Según el Artículo 30 del Código Nacional de Tránsito...",
  "sources": [
    {
      "article_id": "30",
      "title": "Equipos de Prevención y Seguridad",
      "chapter": "Vehículos (Capítulo I, Título IV)"
    }
  ]
}
```

## 🔐 Seguridad

- Las API Keys se manejan mediante variables de entorno
- No se exponen credenciales en el código
- Validación de entrada en el backend

## 🛠️ Desarrollo Local (sin Docker)

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar .env
echo "GEMINI_API_KEY=tu_api_key" > .env

# Levantar ChromaDB por separado
docker run -p 8000:8000 chromadb/chroma:latest

# Ejecutar la app
python app.py
```

## 📚 Datos

Los artículos legales se almacenan en formato JSON en la carpeta `articulos/`. Cada archivo contiene:
- Número de artículo
- Título
- Resumen
- Palabras clave
- Sanciones/multas
- Capítulo

### Indexación automática

Al iniciar la aplicación Flask, se ejecuta automáticamente el script `scripts/index_data.py` que:
1. Lee todos los archivos JSON de la carpeta `articulos/`
2. Vectoriza cada artículo usando Gemini
3. Los guarda en ChromaDB para búsqueda semántica

## 🧪 Tecnologías Utilizadas

- **Backend**: Python 3.10, Flask
- **Base de datos vectorial**: ChromaDB
- **IA**: Google Gemini API
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Contenedores**: Docker, Docker Compose
- **Gestión de entorno**: python-dotenv

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 📧 Contacto

Para preguntas o sugerencias, por favor abre un issue en el repositorio.

---

**⚠️ Disclaimer:** Este asistente proporciona información legal general basada en el Código Nacional de Tránsito. Siempre verifica la información con las autoridades competentes y consulta con un abogado para casos específicos.
