#!/bin/bash

# Proje dizinini bul (çağrıldığı yere göre)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="${DIR}/.."

cd "$PROJECT_ROOT"

echo "CyberLearn Pi - Geliştirme Sunucusu Başlatılıyor..."

# Venv aktivasyonu
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "HATA: 'venv' klasörü bulunamadı. Önce setup.sh betiğini çalıştırın veya 'python3 -m venv venv' ile oluşturun."
    exit 1
fi

export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=1

echo "http://localhost:5000 adresinden erişilebilir."
flask run --host=0.0.0.0 --port=5000
