FROM python:3.8.12-alpine

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt --no-cache-dir

CMD ["python3", "-m", "anisearchdex"]

