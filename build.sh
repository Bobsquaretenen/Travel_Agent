#!/usr/bin/env bash
# Выходим при ошибке
set -o errexit

echo "--- Установка зависимостей ---"
pip install -r requirements.txt

echo "--- Сбор статических файлов ---"
python manage.py collectstatic --no-input

echo "--- Применение миграций ---"
python manage.py migrate

echo "--- Сборка успешно завершена! ---"