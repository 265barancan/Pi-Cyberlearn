from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required
import google.generativeai as genai
import time
from config import Config

ai_bp = Blueprint('ai', __name__)

SYSTEM_PROMPT = """Sen CyberLearn Pi'nin siber güvenlik eğitim asistanısın.
Adın "Cyber-Tutor".
Yalnızca Türkçe cevap ver. Teknik konuları olabildiğince basit, günlük hayattan örneklerle açıkla.
Kesinlikle zararlı, yasa dışı veya saldırı amaçlı (örneğin exploit kodu yazma, hedef sistem hackleme) bilgi verme. 
Eğer kullanıcı böyle bir şey isterse, bunun etik bir laboratuvar dışında yasadışı olduğunu nazikçe hatırlat ve öğretici, savunma odaklı bir konuya yönlendir.
Yanıtların her zaman çok kısa ve öz olmalı.
"""

# Rate limiting için basit in-memory cache
# (Not: Production için Redis düşünülür, ancak Pi'de RAM tasarrufu için dict kullanıyoruz)
user_requests = {}

def get_ai_model():
    if not Config.GEMINI_API_KEY:
        return None
    
    genai.configure(api_key=Config.GEMINI_API_KEY)
    
    # max_output_tokens Pi için kritik
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        system_instruction=SYSTEM_PROMPT,
        generation_config={"max_output_tokens": 500, "temperature": 0.7}
    )
    return model

@ai_bp.route('/')
@login_required
def chat_ui():
    return render_template('ai_tutor.html', api_configured=bool(Config.GEMINI_API_KEY))

@ai_bp.route('/api/chat', methods=['POST'])
@login_required
def chat_api():
    if not Config.GEMINI_API_KEY:
        return jsonify({"error": "Gemini API anahtarı yapılandırılmamış."}), 501
        
    data = request.json
    user_message = data.get("message", "").strip()
    
    if not user_message:
        return jsonify({"error": "Boş mesaj gönderilemez."}), 400
        
    # Basit Rate Limit: Aynı IP/Kullanıcıdan 10 saniyede 1 istek
    now = time.time()
    last_req_time = user_requests.get(request.remote_addr, 0)
    
    if now - last_req_time < 10:
        return jsonify({"error": "Çok hızlı soru soruyorsunuz. Lütfen 10 saniye bekleyin."}), 429
        
    user_requests[request.remote_addr] = now
    
    try:
        model = get_ai_model()
        # Not: Gerçek bir uygulamada sohbet geçmişi session veya DB'de tutulabilir
        # Pi'de hafiflik için tek seferlik (stateless) soru-cevap yapıyoruz
        response = model.generate_content(user_message)
        
        return jsonify({
            "response": response.text,
            "status": "success"
        })
    except Exception as e:
        current_app.logger.error(f"Gemini API Hatası: {str(e)}")
        return jsonify({"error": "Yapay zeka asistanı şu anda yanıt veremiyor. Daha sonra tekrar deneyin."}), 500
