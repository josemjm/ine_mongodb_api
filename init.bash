#! /bin/bash

echo "------ MIGRATE THE DATABASE ------"
python3 manage.py migrate

echo "------ MAKE MIGRATIONS ------"
python3 manage.py makemigrations

echo "------ PARSE AND INSERT DATA ------"
python3 scripts/run_etl.py
echo "------ DATABASE UPDATED ------"

echo "------ RUN SERVER ------"
python3 manage.py runserver 0.0.0.0:8000
