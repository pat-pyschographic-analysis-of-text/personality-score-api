#!/usr/bin/env bash

aws lambda update-function-code \
  --function-name personality-score \
  --zip-file fileb://function.zip
