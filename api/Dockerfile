FROM python:3.10-slim

RUN pip install --upgrade pip 

WORKDIR /app

COPY requirements.txt main.py model_utils.py modelcatb.pkl /app/

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
