FROM tiangolo/uvicorn-gunicorn-starlette:python3.9-slim

ARG MEMCACHED_WORKAROUND

ENV MODULE_NAME="main" \
    VARIABLE_NAME="app"

COPY ./requirements.txt /app/requirements.txt

# Workaround to use memcached
RUN if [ "${MEMCACHED_WORKAROUND}" == "1" ]; then apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*; fi

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app
