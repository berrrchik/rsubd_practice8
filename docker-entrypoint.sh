#!/bin/sh
set -e

echo "=========================================="
echo "Система управления цементным заводом"
echo "Автор: Закляков Даниил Евгеньевич"
echo "Группа: ИКБО-06-22"
echo "=========================================="

mkdir -p /var/log/app

echo "Ожидание готовности MySQL..."
until python -c "import pymysql; pymysql.connect(host='${MYSQL_HOST}', port=int('${MYSQL_PORT}'), user='${MYSQL_USER}', password='${MYSQL_PASSWORD}', database='${MYSQL_DATABASE}') and print('ok')" >/dev/null 2>&1; do
    echo "MySQL ещё не готов, повтор через 2 секунды..."
    sleep 2
done

echo "Запуск Flask-приложения..."
exec python app.py
