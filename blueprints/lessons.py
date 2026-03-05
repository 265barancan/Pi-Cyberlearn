from flask import Blueprint, render_template, redirect, url_for, request, abort, flash
from flask_login import login_required, current_user
import os
import markdown
from config import Config
from models.lesson import Lesson
from models.progress import Progress

lessons_bp = Blueprint('lessons', __name__)

@lessons_bp.route('/')
@login_required
def list_lessons():
    # Redirect to dashboard for now
    return redirect(url_for('index'))

@lessons_bp.route('/<int:lesson_id>')
@login_required
def view_lesson(lesson_id):
    lesson = Lesson.get(lesson_id)
    if not lesson:
        abort(404)
        
    filepath = os.path.join(Config.DATABASE_URI.replace('cyberlearn.db', ''), 'content', 'lessons', lesson.filepath)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            md_content = f.read()
    except FileNotFoundError:
        flash('Ders içeriği bulunamadı.', 'error')
        md_content = "# Hata\n\nDers içeriği dosyası eksik."
        
    # Python-Markdown eklentileriyle HTML'e çevir
    html_content = markdown.markdown(
        md_content,
        extensions=['fenced_code', 'tables']
    )
    
    completed_lessons = Progress.get_completed_lessons(current_user.id)
    is_completed = lesson.id in completed_lessons
    
    return render_template(
        'lesson.html', 
        lesson=lesson, 
        content=html_content,
        is_completed=is_completed
    )

@lessons_bp.route('/<int:lesson_id>/complete', methods=['POST'])
@login_required
def complete_lesson(lesson_id):
    lesson = Lesson.get(lesson_id)
    if not lesson:
        abort(404)
        
    Progress.mark_completed(current_user.id, lesson_id)
    flash(f'{lesson.title} dersini tamamladınız! Tebrikler.', 'success')
    
    # Bir sonraki derse yönlendir (varsitımsal)
    next_lesson = Lesson.get(lesson_id + 1)
    if next_lesson:
        return redirect(url_for('lessons.view_lesson', lesson_id=next_lesson.id))
        
    return redirect(url_for('index'))
