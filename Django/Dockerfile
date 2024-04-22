FROM python:3.11.0-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app
RUN python -m pip install --upgrade pip 
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000