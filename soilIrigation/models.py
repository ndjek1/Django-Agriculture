# soilapp/models.py
from django.db import models

class SoilData(models.Model):
    moisture = models.FloatField()
    temperature = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Moisture: {self.moisture}, Temperature: {self.temperature}"

class IrrigationStatus(models.Model):
    status = models.BooleanField(default=False)
    last_triggered = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Irrigation On" if self.status else "Irrigation Off"
