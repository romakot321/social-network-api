#!/bin/bash
/app/.venv/bin/alembic upgrade head
/app/.venv/bin/gunicorn src.main:app -w 1 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:80 --forwarded-allow-ips="*"
