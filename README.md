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

```bash
pip install alembic
```

```bash
alembic init migrations
```

```bash
alembic revison --autogenerate -m "Initial migration for the user, post and vote tables"
```


## HEROKU

Creating the heroku app

```bash
heroku create fastapi-royalboe
```

The above command creates an heroku app with the name fastapi-royalboe


