from confluent_kafka import Consumer, KafkaException
import json

def consume_messages(topic):
    consumer_config = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'orders-group',
        'auto.offset.reset': 'earliest',  # Start consuming from the earliest message
    }
    
    consumer = Consumer(consumer_config)

    try:
        consumer.subscribe([topic])
        print(f"Subscribed to topic: {topic}")

        while True:
            msg = consumer.poll(timeout=1.0)  # Poll for new messages
            if msg is None:  # No message received
                continue
            if msg.error():
                if msg.error().code() == KafkaException._PARTITION_EOF:
                    print("End of partition reached")
                else:
                    print(f"Error: {msg.error()}")
                continue

            # Decode and process the message
            message_value = json.loads(msg.value().decode('utf-8'))
            print(f"Consumed message: {message_value}")

    except KeyboardInterrupt:
        print("Consumer interrupted by user")
    finally:
        consumer.close()

if __name__ == "__main__":
    consume_messages('orders')  