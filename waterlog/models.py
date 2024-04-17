from django.db import models

class Plant(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100)
    last_watered = models.DateField(auto_now_add=True)
    watering_interval = models.IntegerField(help_text="Enter number of days between watering")

    def __str__(self):
        return self.name

class WaterLog(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    watered_at = models.DateTimeField()

    def __str__(self):
        return f"{self.plant.name} watered on {self.watered_at.strftime('%Y-%m-%d %H:%M')}"
