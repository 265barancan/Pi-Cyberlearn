<div align="center">
  <h1>🛡️ CyberLearn Pi</h1>
  <p><strong>Raspberry Pi ve düşük donanımlı cihazlar için optimize edilmiş, hafif ve interaktif siber güvenlik eğitim platformu.</strong></p>
  
  [![Python version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
  [![Flask](https://img.shields.io/badge/Flask-3.0.3-black)](https://flask.palletsprojects.com/)
  [![Gemini AI](https://img.shields.io/badge/Google%20Gemini-AI%20Tutor-blueviolet)](https://ai.google.dev/)
  [![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
</div>

<br />

## 📖 Proje Hakkında (Description)

**CyberLearn Pi**, ARM tabanlı düşük donanımlı sistemlerde (Örn: *Raspberry Pi 1 Type B - 512 MB RAM*) dahi akıcı ve sorunsuz çalışmasını sağlamak amacıyla en temel, hızlı teknolojiler kullanılarak oluşturulmuş projedir. Öğrencilere ağ güvenliği, şifreleme ve komut satırı temellerini güvenli bir sanal alanda öğretir. Vanilla JS, derlenmiş TailwindCSS ve hafif bir SQLite-Flask mimarisi kullanılarak ayağa kaldırılmıştır.

## ✨ Temel Özellikler

- 📚 **Modüler Ders İçerikleri:** Markdown destekli çevrimdışı çalışabilen eğitim dökümanları.
- 💻 **Bütünleşik Terminal Simülatörü:** Öğrencilerin Linux komutlarını, gerçek bir sunucuya zarar verme riski olmadan güvenle deneyimleyebildiği yerel JS simülatörü.
- 🤔 **Etkileşimli Quiz Motoru:** Modül sonlarında öğrenmeyi pekiştiren, anlık geri bildirimli, sayfa yenilemeden (AJAX) çalışan soru bankası.
- 🤖 **Cyber-Tutor (Siber Asistan):** Google Gemini 1.5 Pro tabanlı eğitim asistanı. (Donanım maliyetleri düşünülerek token optimizasyonu ile kurgulanmıştır).
- ⚡ **Yüksek Performans:** Node.js, ağır SPA (Single Page Application) frameworkleri ve devasa veritabanları yerine Vanilla JS, SQLite ve Flask-Gunicorn yapısıyla (maks. 2 asenkron worker) optimize edilmiştir.
- 🔒 **Güvenli Erişim:** Flask-Login ile kontrol edilen kullanıcı kimlik doğrulama paneli.

---

## 🚀 Hızlı Başlangıç & Kurulum

Linux veya macOS dağıtımları üzerinde hızlıca kurmak için otomatik kurulum betiğini kullanabilirsiniz:

```bash
# Projeyi bilgisayarınıza/sunucunuza indirin
git clone [GITHUB-REPO-LINK]
cd cyberlearn-pi

# Kurulum scriptine yetki verin ve başlatın
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### 🛠️ Manuel Geliştirici Kurulumu

Eğer kurulum betiğini kullanmak istemezseniz, aşağıdaki standart adımları takip edin:

**1. Sanal ortamı hazırlayın:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**2. Veritabanını başlatın ve ilk verileri girin:**
```bash
python3 scripts/seed_db.py
```

**3. API Anahtarlarını belirleyin:**
- Klasördeki `.env.example` dosyasının adını `.env` olarak değiştirin ve uygun alanları (Gemini API Secret vb.) doldurun.

**4. Canlı geliştirme sunucusunu çalıştırın:**
```bash
bash scripts/dev_server.sh
```
Uygulama `http://localhost:5000` adresinden erişilebilir olacaktır.

---

## 🏗️ Proje Mimarisi & Dizin Yapısı

- `app.py`: Ana Flask uygulama başlangıç dosyası.
- `blueprints/`: Uygulamanın alan adlarına göre (Auth, Quiz, Lesson, vb.) ayrılmış Controller (rotalandırma) yapıları.
- `models/`: Kullanıcı verilerini tutan SQLite3 (SQLAlchemy olmadan, hafif) veritabanı tabloları.
- `content/lessons/`: Ders içeriklerinin depolandığı Markdown (.md) havuzu.
- `static/js/`: Eğitim paneli, terminal simülatörü ve quiz etkileşimlerinden sorumlu Vanilla Javascript dosyaları.

## 🤝 Katkıda Bulunma

Geliştirmeye katkıda bulunmak isteyen herkes için pull request'ler her zaman açıktır. Ancak, projeye kütüphane eklerken cihazların RAM sınırlarını (maksimum 512 MB) hesaba kattığımızdan lütfen gereksiz npm / pip paketlerini projeye dahil etmekten kaçının.

## 📄 Lisans

Bu proje **MIT** lisansı altında dağıtılmaktadır. Daha fazla bilgi için `LICENSE` dosyasına bakabilirsiniz.
