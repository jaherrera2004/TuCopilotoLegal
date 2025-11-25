from flask import Blueprint, request, jsonify
from services.chat_service import ChatService

chat_bp = Blueprint('chat', __name__)

chat_service = ChatService()

@chat_bp.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')
    
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    try:
        result = chat_service.get_response(user_message)
        return jsonify(result)

    except Exception as e:
        print(f"Error en chat: {e}")
        return jsonify({"error": "Ocurrió un error procesando tu solicitud."}), 500
