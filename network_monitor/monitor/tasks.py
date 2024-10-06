from celery import shared_task
from .models import NetworkFrequency

@shared_task
def preprocess_data(data):
    # Simulate data cleaning and normalization
    frequency = clean_frequency(data['frequency'])
    NetworkFrequency.objects.create(timestamp=data['timestamp'], frequency=frequency)

def clean_frequency(frequency):
    # Simulated cleaning step
    return round(frequency, 2)
