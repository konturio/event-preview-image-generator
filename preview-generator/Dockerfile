FROM python:3.9-slim

ARG MEMCACHED_WORKAROUND

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

# Workaround to use memcached
RUN if [ "${MEMCACHED_WORKAROUND}" = "1" ]; then apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*; fi

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app

ENTRYPOINT uvicorn main:app --host 0.0.0.0 --port ${PORT}