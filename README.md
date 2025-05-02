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
