# Commands ran

## This is to create a virtual environment

```bash
py -3 -m venv venv
```

## To activate it

```bash
source venv/Scripts/activate
```

## Install FAstAPI

```bash
pip install fastapi[all]
```

## To run the api

The unicorn runs the fastapi instance, main is the name of the python file that serves as the entry point while app is the instance of the fastAPI to run

```bash
uvicorn main:app
```

```bash
uvicorn app.main:app --reload
```

## To removed previously tracked files

```bash
git rm -r --cached .
```

## Database format

"postgresql://<username>:<password>@<ip-addr>:<port>/<DB_NAME>"

## Alembic

Using pip to install alembic for database migration

```bash
pip install alembic
```

Initializing migration using a directory named migrations instead of default alembic

```bash
alembic init migrations
```

After configuring the alembic.ini file and env.py files, we can autogenerate revisions with the command below

```bash
alembic revison --autogenerate -m "Initial migration for the user, post and vote tables"
```

Example of how to add a revision

```bash
alembic revision -m 'eg adding users'
```

To see the current revision

```bash
alembic current
```

To check revision history

```bash
alembic history
```

To apply the revision

```bash
alembic upgrade head
alembic upgrade <revision>
alembic upgrade +1 or =2 etc
```

To downgrade to a previosu revision

```bash
alembic downgrade -1
```

```bash
alembic downgrade <revision>
```

## Deploy to Heroku

Login to heroku

```bash
heroku login
```

Creating the heroku app

```bash
heroku create fastapi-royalboe
```

To commit to heroku main

```bash
git push heroku main
```

To restart heroku app

```bash
heroku ps:restart
```

To create database

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

To check logs

```bash
heroku logs -t
```

To run migration for the applications after inputing necessary credentials

```bash
heroku run alembic upgrade head
```

To view url in chrome

```bash
heroku open
```

To destroy addons

```bash
heroku addons:destroy heroku-postgresql
```


## Deploy to A VM in the cloud

Spin up virtual machine on the cloud
Log in to the virtual machine as root

Run the following commands in the ubuntu machine

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install libpq-dev -y
sudo apt install python3-pip -y
sudo apt install python3-virtualenv -y
sudo apt install postgresql postgresql-contrib -y
```

Switch to postgres user

```bash
su - postgres
```

Go into posgres and change paswword for postgres db user

```bash
psql
```

```psql
\password
```

Quit psql

```psql
\q
```

Go back to root user

```bash
exit
```

in root user, make adjustments to postgresql.conf file to allow remote connections, change peer to md5

```bash
vi /etc/postgresql/<version>/main/postgresql.conf
vi /etc/postgresql/<version>/main/pg_hba.conf
```

Create a new user

```bash
adduser fastapi
```

Add user to sudoer group

```bash
usermod -aG sudo fastapi
```

Create a folder and add a virtual environment

```bash
mkdir app
virtualenv fastenv
source fastenv/bin/activate
```

Clone the project

```bash
git clone https://github.com/royalboe/fast_api.git .
```

Install dependencies

```bash
pip install -r requirements.txt
```

Handle the environment variables

```bash
vi /home/fastapi/.env
set -o allexport; source /home/fastapi/.env; set +o allexport
```

Persist env

```bash
echo 'set -o allexport; source /home/fastapi/.env; set +o allexport' >> /home/fastapi/.profile
```

Run the application

```bash
uvicorn --host 0.0.0.0 --port 8080 app.main:app
```

or

```bash
fastapi run app/main.py
```

or 

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8080
```

Make a service for the file

```bash
sudo cp gunicorn.service /etc/systemd/system/fastapi.service
```

Install nginx and use the cofiguaration file in the repo

```bash
sudo apt install nginx -y
```

TLS encryption

```bash
sudo snap install --classic certbot
sudo certbot --nginx
```

Firewall

```bash
sudo ufw allow http
sudo ufw allow 8000
sudo ufw allow https
sudo ufw allow ssh
sudo ufw allow 5432
sudo ufw enable
sudo ufw status
```

To delete

```bash
sudo ufw delete allow 8000
```

## Docker

Used docker compose watch to make changes in development

```bash
docker-compose -f docker-compose-dev.yml --build --watch
```

## For testing

Install pytest

```bash
pip install pytest
```

use pytest to run tests; make sure tests have the test_ prefix to get automatically detected. Also the -v is to list the passed tests.
To see printing statements add -s option and -x to stop after the first failure.

```bash
pytest -v
```

```bash
pytest --disable-warnings
```

```bash
pytest -v --disable-warnings -x -s
```

