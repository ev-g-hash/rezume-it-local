#!/bin/bash

echo "🚀 Подготовка к деплою на Amvera Cloud..."

# Очищаем кэш
echo "🧹 Очистка кэша..."
find . -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
rm -rf .pytest_cache 2>/dev/null || true
rm -rf htmlcov 2>/dev/null || true

# Создаем .env файл если его нет
if [ ! -f .env ]; then
    echo "📝 Создание файла .env..."
    cat > .env << EOF
# Django Settings
DJANGO_SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(50))")
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=*

# Database (SQLite)
DJANGO_DB_PATH=/data/db.sqlite3
EOF
    echo "✅ Файл .env создан с настройками по умолчанию"
    echo "⚠️  ВНИМАНИЕ: Отредактируйте файл .env перед деплоем!"
fi

# Проверяем миграции
echo "🗄️ Проверка миграций..."
python manage.py makemigrations --check || python manage.py makemigrations

# Применяем миграции
echo "📦 Применение миграций..."
python manage.py migrate

echo ""
echo "✅ Проект готов к деплою!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Загрузите проект в Git репозиторий"
echo "2. Подключите репозиторий в Amvera Cloud"
echo "3. Настройте переменные окружения в Amvera:"
echo "   - DJANGO_SECRET_KEY: ваш секретный ключ"
echo "   - DJANGO_DEBUG: False (обязательно)"
echo "   - DJANGO_ALLOWED_HOSTS: ваш домен или *"
echo "4. Запустите деплой"
echo ""
echo "🔐 Для генерации нового SECRET_KEY выполните:"
echo "   python -c \"import secrets; print(secrets.token_urldata())\""