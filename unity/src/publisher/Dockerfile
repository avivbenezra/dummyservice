FROM python:3.8-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir flask kafka-python
EXPOSE 5000
CMD ["python", "publisher.py"]
