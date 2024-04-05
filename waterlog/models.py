from django.db import models

class Plant(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class WaterLog(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, null=True)
    watered_at = models.DateTimeField(auto_now_add=True, verbose_name="Watered At")
    message_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="Telegram Message ID")

    def __str__(self):
        # Return a string that includes the plant name and the watering timestamp
        return f"{self.plant.name} watered at {self.watered_at}"
