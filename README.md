# microservice

# 1. Contact Service
## Go to the project folder
cd contacts /
## Install and run the virtual environment
python3.7 -m venv .env
source .env / bin / activate

## Install dependencies
pip install -r contact_requirements.txt

## Create migration and migrate the data in postgres database 
## Before starting migrations,postgres must be installed and configured
python manage.py makemigrations
python manage.py migrate

## run the server using 
python manage.py runserver


