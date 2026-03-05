from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.find_by_username(username)
        
        if not user or not check_password_hash(user.password_hash, password):
            flash('Kullanıcı adı veya şifre hatalı.', 'error')
            return redirect(url_for('auth.login'))
            
        login_user(user)
        return redirect(url_for('index'))
        
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.find_by_username(username)
        
        if user:
            flash('Bu kullanıcı adı zaten alınmış.', 'error')
            return redirect(url_for('auth.register'))
            
        User.create(username, generate_password_hash(password, method='scrypt'))
        flash('Kayıt başarılı, lütfen giriş yapın.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
