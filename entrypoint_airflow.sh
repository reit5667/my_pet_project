#!/usr/bin/env bash
set -e
# Ждём готовности БД, выставляем логин/пароль для UI (admin/admin или airflow/admin)
until airflow db check 2>/dev/null; do echo "Waiting for DB..."; sleep 3; done
# Создаём admin или сбрасываем пароль; standalone иногда создаёт airflow
airflow users create --username admin --firstname Admin --lastname User --role Admin \
  --email admin@example.com --password admin 2>/dev/null || true
airflow users reset-password -u admin -p admin 2>/dev/null || true
airflow users reset-password -u airflow -p admin 2>/dev/null || true
exec airflow standalone
