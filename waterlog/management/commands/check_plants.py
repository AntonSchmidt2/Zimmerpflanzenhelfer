# waterlog/management/commands/check_plants.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from waterlog.models import Plant, WaterLog
from waterlog.utils import send_notification, delete_notification
from django.db.models import Max


class Command(BaseCommand):
    help = 'Check for plants that haven’t been watered for 7 days'

    def handle(self, *args, **kwargs):
        threshold_date = timezone.now() - timedelta(days=7)
        plants_to_notify = Plant.objects.annotate(
            latest_watering=Max('waterlog__watered_at')
        ).filter(
            latest_watering__lte=threshold_date
        )

        for plant in plants_to_notify:
            message_id = send_notification(plant)

            # Create a WaterLog instance for the plant with the message_id
            if message_id:
                WaterLog.objects.create(plant=plant, message_id=message_id)
                self.stdout.write(self.style.WARNING(f"Notified for {plant.name}"))