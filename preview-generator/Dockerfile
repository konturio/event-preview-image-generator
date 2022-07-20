FROM tiangolo/uvicorn-gunicorn-starlette:python3.9

ENV MODULE_NAME="main" \
    VARIABLE_NAME="app"

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app
