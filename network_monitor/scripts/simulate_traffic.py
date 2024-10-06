from kafka import KafkaProducer
import json
import random
import time

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

while True:
    data = {
        'timestamp': time.time(),
        'frequency': random.uniform(47.0, 53.0)
    }
    producer.send('network-frequency', value=data)
    time.sleep(1)
