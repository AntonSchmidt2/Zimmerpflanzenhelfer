from django.db import models
from datetime import datetime

class Plant(models.Model):
    name = models.CharField(max_length=100, default="SomePlant")
    species = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, null=True)
    last_watered = models.DateField(auto_now_add=True, null=True)
    watering_interval = models.IntegerField(help_text="Enter number of days between watering", default=7)  # default set to 7 days
    def __str__(self):
        return self.name

class WaterLog(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, null=True)  # Making 'plant' nullable
    watered_at = models.DateTimeField(default=datetime.now)  # Default value for 'watered_at'

    def __str__(self):
        return f"{self.plant.name} watered on {self.watered_at.strftime('%Y-%m-%d %H:%M')}"
