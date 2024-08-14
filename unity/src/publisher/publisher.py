from flask import Flask, request, jsonify
from kafka import KafkaProducer
import json

app = Flask(__name__)

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',  # Kafka broker
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize data as JSON
)

# Global variable to keep track of statistics
stats_data = {
    'kafka_messages_sent': 0
}

@app.route('/publish', methods=['POST'])
def publish_message():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        # Send data to Kafka topic
        producer.send('data_topic', value=data)
        stats_data['kafka_messages_sent'] += 1  # Increment the counter
        return jsonify({'status': 'Message published successfully'}), 200
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
    app.run(host='0.0.0.0', port=5000)
