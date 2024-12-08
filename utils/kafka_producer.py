from confluent_kafka import Producer
import json


def get_kafka_producer():
    producer_config = {
        'bootstrap.servers': 'localhost:9092',  # Kafka broker address
    }
    return Producer(producer_config)


def delivery_report(err, msg):
    """
    Callback for delivery reports from the broker.
    This method will be called for each message produced.
    """
    if err:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")


def send_message(topic, message):
    producer = get_kafka_producer()

    try:
        # Serialize the message to JSON
        serialized_message = json.dumps(message)

        # Send the message with a callback to check delivery status
        producer.produce(topic, value=serialized_message, callback=delivery_report)

        # Ensure all messages are delivered before exiting
        producer.flush()
        print(f"Message sent to topic '{topic}': {message}")
    except Exception as e:
        print(f"Failed to send message: {e}")
