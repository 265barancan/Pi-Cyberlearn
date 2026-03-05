# CyberLearn Pi

**CyberLearn Pi**, özellikle **Raspberry Pi 1 Type B** gibi düşük RAM ve CPU kapasitesine sahip cihazlar üzerinde çalışabilmesi için tasarlanmış siber güvenlik eğitim platformudur. Uygulama Vanilla JS, Tailwind CSS, Flask ve SQLite kullanılarak ultra hafif olarak geliştirilmiştir.

## Özellikler

- **Modüler Ders Sistemi:** Siber güvenlik temelleri, ağ bilgisi, Linux ve kriptografi üzerine Markdown formatında hazırlanan dersler.
- **Sanal Terminal Simülatörü:** Öğrencilerin ağ izole edilmiş güvenli bir ortamda komut denemeleri yapmasını sağlayan tarayıcı tabanlı terminal. (komut beyaz listesi üzerinden çalışır).
- **Etkileşimli Quiz Motoru:** JS tabanlı anlık geri bildirim veren soru çözümleme motoru.
- **Cyber-Tutor (Gemini AI):** Google Gemini 1.5 Pro tabanlı eğitim asistanı. (Bağlamı korumadan API maliyetlerini düşüren basit entegrasyon)
- **Kullanıcı İlerleme Takibi:** Kayıt, giriş ve ders tamamlama oranlarının takibi.

## Kurulum (Raspberry Pi veya Ubuntu)

Otomatik kurulum betiği ile projeyi hızlıca çalıştırabilirsiniz:

```bash
cd cyberlearn-pi
chmod +x scripts/setup.sh
./scripts/setup.sh
```

## Manuel Kurulum

1. Sanal ortamı hazırlayın:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. `.env` dosyasını oluşturun:
   ```bash
   cp .env.example .env
   # GEMINI_API_KEY değerini dotenv dosyasına ekleyin.
   ```

3. Veritabanını oluşturun:
   ```bash
   python3 scripts/seed_db.py
   ```

4. Geliştirme Sunucusunu Başlatın:
   ```bash
   bash scripts/dev_server.sh
   # Uygulama http://localhost:5000 / http://<raspberry-pi-ip>:5000 adresinde çalışacaktır.
   ```

## Production İpuçları
Nginx reverse proxy kullanmanız ve asenkron hizmet için gunicorn'u 2 worker ile çalıştırmanız (RAM tüketimi için max 2) önerilir:
```bash
gunicorn app:app --workers 2 --worker-class sync --bind 0.0.0.0:5000
```
