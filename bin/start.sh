#!/bin/sh
uvicorn src.main:app --reload --host 0.0.0.0 --port=8080 --no-access-log --log-level=critical