#!/usr/bin/env bash
# Выходим при ошибке
set -o errexit

echo "--- Установка зависимостей ---"
pip install -r requirements.txt

echo "--- Сбор статических файлов ---"
python manage.py collectstatic --no-input

echo "--- Применение миграций ---"
python manage.py migrate

echo "--- Создание суперпользователя (если он еще не создан) ---"
# Берет логин, email и пароль из переменных окружения Render
# '|| true' предотвращает падение сборки, если суперпользователь уже существует
python manage.py createsuperuser --noinput || true

echo "--- Сборка успешно завершена! ---"