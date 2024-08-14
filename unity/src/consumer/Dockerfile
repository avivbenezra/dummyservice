FROM python:3.8-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir flask kafka-python pymongo
EXPOSE 5001
CMD ["python", "consumer.py"]
