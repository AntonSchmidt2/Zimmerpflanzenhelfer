from django.db import models

class WaterLog(models.Model):
    plant_name = models.CharField(max_length=100)
    watered_at = models.DateTimeField()

    def __str__(self):
        return self.plant_name
