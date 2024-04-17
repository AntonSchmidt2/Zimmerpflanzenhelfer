from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from waterlog.models import Plant, WaterLog
from waterlog.utils import send_notification
from django.db.models import Max, F, ExpressionWrapper, DateTimeField

class Command(BaseCommand):
    help = 'Check for plants that haven’t been watered for 7 days'

    def handle(self, *args, **kwargs):
        # Adjusted to ensure timezone.now() is used in comparison correctly
        threshold_date = timezone.now() - timedelta(days=7)

        # Ensuring the annotated 'latest_watering' is correctly processed
        plants = Plant.objects.annotate(
            latest_watering=Max('waterlog__watered_at')
        )

        # Filter after annotation to ensure comparison is against Python datetime
        plants_to_notify = [plant for plant in plants if plant.latest_watering and plant.latest_watering <= threshold_date]

        for plant in plants_to_notify:
            message_id = send_notification(plant)
            if message_id:
                WaterLog.objects.create(plant=plant, watered_at=timezone.now(), message_id=message_id)
                self.stdout.write(self.style.WARNING(f"Notified for {plant.name}"))
