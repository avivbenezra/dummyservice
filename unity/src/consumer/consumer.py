from flask import Flask, jsonify
from kafka import KafkaConsumer
import json
import pymongo

app = Flask(__name__)

# Initialize MongoDB Client
client = pymongo.MongoClient("mongodb://mongodb:27017/")
db = client["mydatabase"]
collection = db["mycollection"]

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    'data_topic',  # Kafka topic
    bootstrap_servers='kafka:9092',  # Kafka broker
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # Deserialize data from JSON
)

# Global variable to keep track of statistics
stats_data = {
    'kafka_messages_received': 0,
    'mongo_inserts': 0
}

@app.route('/consume', methods=['GET'])
def consume_message():
    try:
        for message in consumer:
            # Insert the message value into MongoDB
            collection.insert_one(message.value)
            stats_data['kafka_messages_received'] += 1  # Increment Kafka message count
            stats_data['mongo_inserts'] += 1            # Increment MongoDB insert count
        return jsonify({'status': 'Messages consumed and inserted into MongoDB'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stats', methods=['GET'])
def stats():
    return jsonify(stats_data), 200

@app.route('/health', methods=['GET'])
def health():
    # Simple health check endpoint
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
