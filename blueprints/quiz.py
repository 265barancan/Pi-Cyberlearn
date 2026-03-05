from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required
from models.database import get_db
import google.generativeai as genai
from config import Config
import json
import re

quiz_bp = Blueprint('quiz', __name__)

# Pi RAM tasarrufu için basit in-memory önbellek (Sınırlı kapasite)
# [module_id] -> [ {id: 1, question: "...", options: [], correct_index: 0, explanation: ""} ]
quiz_cache = {}

def generate_quiz_array(module_id):
    if not Config.GEMINI_API_KEY:
        return None
        
    genai.configure(api_key=Config.GEMINI_API_KEY)
    
    prompt = f"""
    Sen CyberLearn eğitim platformunun bir quiz hazırlayıcısısın.
    'Modül {module_id}' (Siber güvenlik temelleri) ile ilgili temel seviyede 3 adet çoktan seçmeli soru oluştur.
    LÜTFEN ÇIKTIYI SADECE VE SADECE AŞAĞIDAKİ JSON YAPISINDA VER, BAŞKA HİÇBİR METİN VEYA MD ETİKETİ EKLEME:
    [
      {{
        "id": 1,
        "question": "Soru metni",
        "options": ["Şık A", "Şık B", "Şık C", "Şık D"],
        "correct_index": 0,
        "explanation": "Neden A şıkkının doğru olduğuna dair çok kısa açıklama."
      }}
    ]
    Yalnızca JSON formatında dizi döndür. Başka hiçbir şey ekleme.
    """
    
    model = genai.GenerativeModel("gemini-1.5-pro", generation_config={"temperature": 0.5})
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Olası Markdown `json` bloklarını temizle
        if text.startswith('```'):
            text = re.sub(r'^```(json)?|```$', '', text, flags=re.MULTILINE).strip()
            
        questions = json.loads(text)
        
        # ID'leri eşsizleştir (Basit güvenlik önlemi)
        for i, q in enumerate(questions):
            q['id'] = int(f"{module_id}00{i+1}")
            
        return questions
    except Exception as e:
        current_app.logger.error(f"Quiz Üretim Hatası (Gemini): {e}")
        return None

@quiz_bp.route('/<int:module_id>')
@login_required
def view_quiz(module_id):
    return render_template('quiz.html', module_id=module_id)

@quiz_bp.route('/api/questions/<int:module_id>')
@login_required
def get_questions(module_id):
    # Eğer bu modül için önbellekte soru varsa onu dön
    if module_id in quiz_cache:
        questions_without_answers = [
            {"id": q["id"], "question": q["question"], "options": q["options"]} 
            for q in quiz_cache[module_id]
        ]
        return jsonify(questions_without_answers)
        
    # Yoksa Gemini'den yeni yarat
    new_questions = generate_quiz_array(module_id)
    
    if not new_questions:
        return jsonify({"error": "Sorular şu an oluşturulamadı. (API Anahtarını kontrol edin)"}), 500
        
    # Önbelleğe kaydet (Cevap anahtarıyla birlikte)
    quiz_cache[module_id] = new_questions
    
    # Kullanıcıya sadece soruları (Cevap anahtarı olmadan) dön
    questions_without_answers = [
        {"id": q["id"], "question": q["question"], "options": q["options"]} 
        for q in new_questions
    ]
    
    return jsonify(questions_without_answers)

@quiz_bp.route('/api/submit', methods=['POST'])
@login_required
def submit_answer():
    data = request.json
    module_id = data.get('module_id')
    question_id = data.get('question_id')
    selected_index = data.get('selected_index')
    
    if module_id not in quiz_cache:
        return jsonify({"error": "Modül oturumu bulunamadı. Lütfen sayfayı yenileyin."}), 400
        
    question = next((q for q in quiz_cache[module_id] if q["id"] == question_id), None)
    
    if not question:
        return jsonify({"error": "Soru numarası geçersiz."}), 400
        
    is_correct = (question["correct_index"] == selected_index)
    
    return jsonify({
        "is_correct": is_correct,
        "correct_index": question["correct_index"],
        "explanation": question["explanation"]
    })
