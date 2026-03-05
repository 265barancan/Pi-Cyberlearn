#!/bin/bash
echo "CyberLearn Pi - Kurulum Betiği Başlatılıyor..."

# PiOS için gerekli sistem paketleri
echo "Gerekli sistem paketleri kontrol ediliyor (sudo erişimi gerekebilir)..."
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="${DIR}/.."
cd "$PROJECT_ROOT"

# Sanal ortam
if [ ! -d "venv" ]; then
    echo "Sanal ortam (venv) oluşturuluyor..."
    python3 -m venv venv
fi

echo "Bağımlılıklar yükleniyor..."
source venv/bin/activate
pip install -r requirements.txt

# DB Oluşturma
echo "Veritabanı oluşturuluyor..."
python3 scripts/seed_db.py

# Ortam değişkenleri kopyalanıyor (Yoksa)
if [ ! -f ".env" ]; then
    echo ".env dosyası oluşturuluyor (Lütfen daha sonra GEMINI_API_KEY ekleyin)..."
    cp .env.example .env
fi

echo "Kurulum tamamlandı! Geliştirmeye başlamak için:"
echo "bash scripts/dev_server.sh"
