FROM python:3.11

WORKDIR /app

COPY service1/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY proto /app/proto
COPY service1 /app/service1

WORKDIR /app/service1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
