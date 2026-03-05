from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models.database import get_db

quiz_bp = Blueprint('quiz', __name__)

# Örnek statik veri (Raspberry Pi SQLite'ında tablo yaratmak yerine hafif kalması için array)
QUIZ_DATA = {
    1: [
        {
            "id": 101,
            "question": "Aşağıdakilerden hangisi bir IP adresi örneğidir?",
            "options": ["http://google.com", "192.168.1.1", "00:1A:2B:3C:4D:5E", "8080"],
            "correct_index": 1,
            "explanation": "IP adresleri ağdaki cihazları tanımlayan, noktalarla ayrılmış sayısal dizilerdir."
        },
        {
            "id": 102,
            "question": "HTTP ve HTTPS arasındaki temel fark nedir?",
            "options": [
                "HTTP daha hızlıdır", 
                "HTTPS sadece mobilde çalışır", 
                "HTTPS verileri şifreleyerek iletir", 
                "Hiçbir fark yoktur"
            ],
            "correct_index": 2,
            "explanation": "HTTPS (S=Secure), HTTP trafiğinin SSL/TLS ile şifrelenmiş halidir."
        }
    ]
}

@quiz_bp.route('/<int:module_id>')
@login_required
def view_quiz(module_id):
    if module_id not in QUIZ_DATA:
        return "Quiz bulunamadı", 404
        
    return render_template('quiz.html', module_id=module_id)

@quiz_bp.route('/api/questions/<int:module_id>')
@login_required
def get_questions(module_id):
    if module_id not in QUIZ_DATA:
        return jsonify({"error": "Soru bulunamadı"}), 404
        
    questions_without_answers = []
    for q in QUIZ_DATA[module_id]:
        q_clean = {"id": q["id"], "question": q["question"], "options": q["options"]}
        questions_without_answers.append(q_clean)
        
    return jsonify(questions_without_answers)

@quiz_bp.route('/api/submit', methods=['POST'])
@login_required
def submit_answer():
    data = request.json
    module_id = data.get('module_id')
    question_id = data.get('question_id')
    selected_index = data.get('selected_index')
    
    if module_id not in QUIZ_DATA:
        return jsonify({"error": "Modül geçersiz"}), 400
        
    question = next((q for q in QUIZ_DATA[module_id] if q["id"] == question_id), None)
    
    if not question:
        return jsonify({"error": "Soru geçersiz"}), 400
        
    is_correct = (question["correct_index"] == selected_index)
    
    return jsonify({
        "is_correct": is_correct,
        "correct_index": question["correct_index"],
        "explanation": question["explanation"]
    })
