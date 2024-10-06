from celery import shared_task
from .models import NetworkFrequency
import numpy as np 
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_alert(frequency):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'alerts',
        {
            'type': 'frequency_alert',
            'message': f'Anomaly detected: {frequency} Hz',
        }
    )


def detect_anomalies(frequency):
    recent_data = NetworkFrequency.objects.all().order_by('-timestamp')[:100]  # Last 100 records
    if len(recent_data) < 2:
        return False  # Not enough data
    mean = np.mean([record.frequency for record in recent_data])
    std_dev = np.std([record.frequency for record in recent_data])
    z_score = (frequency - mean) / std_dev
    return abs(z_score) > 3  # Anomaly if Z-score is > 3

@shared_task
def preprocess_data(data):
    frequency = clean_frequency(data['frequency'])
    anomaly = detect_anomalies(frequency)
    NetworkFrequency.objects.create(timestamp=data['timestamp'], frequency=frequency, anomaly_detected=anomaly)

    if anomaly:
        send_alert(frequency)

def clean_frequency(frequency):
    # Simulated cleaning step
    return round(frequency, 2)
