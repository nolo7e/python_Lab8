FROM python:3.11

WORKDIR /app

COPY service2/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY proto /app/proto
COPY service2 /app/service2

WORKDIR /app/service2

CMD ["sh", "-c", "python populate_db.py && python server.py"]