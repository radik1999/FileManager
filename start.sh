#!/bin/sh

pip install -r requirements.txt
uvicorn app.main:app --host localhost --port 8080