import sqlite3
import os
import sys

# Proje kök dizinine erişim
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config
from werkzeug.security import generate_password_hash

def seed():
    print("Veritabanı oluşturuluyor ve başlangıç verileri ekleniyor...")
    
    db_path = Config.DATABASE_URI
    
    # Mevcut DB varsa sil (Sıfırlama işlemi)
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Eski veritabanı silindi.")
        
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Şemayı yükle
    with open(os.path.join(os.path.dirname(__file__), '../schema.sql'), 'r') as f:
        cur.executescript(f.read())
        
    print("Şema başarıyla yüklendi.")
    
    # Örnek Kullanıcılar
    password_hash = generate_password_hash("123456", method="scrypt")
    cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", ("student", password_hash))
    cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", ("admin", password_hash))
    
    # Ders İçerikleri
    lessons = [
        ("Ağ Temellerine Giriş", "01-temel-aglar.md", 1, 1),
        ("Linux Komut Satırı", "02-linux-temelleri.md", 1, 2),
        ("Nmap ile Port Tarama", "03-nmap-kavramlari.md", 2, 1),
        ("Kriptografi 101", "04-sifreleme.md", 3, 1),
    ]
    
    for title, filepath, module, order in lessons:
        cur.execute(
            "INSERT INTO lessons (title, filepath, module, order_index) VALUES (?, ?, ?, ?)",
            (title, filepath, module, order)
        )
        # Dummy dosya oluştur
        lesson_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../content/lessons/', filepath))
        if not os.path.exists(lesson_path):
            with open(lesson_path, 'w') as lf:
                lf.write(f"# {title}\n\nBu dosya otomatik olarak oluşturulmuştur.")
                
    print(f"{len(lessons)} ders veritabanına eklendi.")
    
    conn.commit()
    conn.close()
    print("Veritabanı başlatma tamamlandı! ✨")

if __name__ == '__main__':
    seed()
