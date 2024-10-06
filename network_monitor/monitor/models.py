from django.db import models

class NetworkFrequency(models.Model):
    timestamp = models.DateTimeField()
    frequency = models.FloatField()
    cleaned = models.BooleanField(default=True)
    anomaly_detected = models.BooleanField(default=False)