# Flask Dockerfile
FROM python:3.10-alpine as base

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]