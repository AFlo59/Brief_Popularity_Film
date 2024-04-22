FROM python:3.11.0-slim

RUN pip install --upgrade pip 

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt

EXPOSE 8080

#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
