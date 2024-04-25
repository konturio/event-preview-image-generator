FROM python:3.9-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*;
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app

ENTRYPOINT uvicorn main:create_app --factory --host 0.0.0.0 --port ${PORT}
