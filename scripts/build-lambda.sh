#!/usr/bin/env bash

mkdir -p lambda
pipenv lock -r > requirements.txt
pip install -r requirements.txt --no-deps -t lambda
zip -r function.zip lambda
zip -r function.zip *.py
