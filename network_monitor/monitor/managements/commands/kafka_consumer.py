from kafka import KafkaConsumer
import json
from django.core.management.base import BaseCommand
from monitor.tasks import preprocess_data

class Command(BaseCommand):
    help = 'Consume data from Kafka'

    def handle(self, *args, **kwargs):
        consumer = KafkaConsumer(
            'network-frequency',
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

        for message in consumer:
            data = message.value
            preprocess_data.delay(data)
