import json
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from waterlog.models import WaterLog
import telegram
import os
from django.conf import settings
from django.db.models import Max
import asyncio
from telegram.ext import Application


config_path = os.path.join(settings.BASE_DIR, 'config.json')
with open(config_path) as config_file:
    config = json.load(config_file)

TELEGRAM_BOT_TOKEN = config.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = config.get('TELEGRAM_CHAT_ID')


class Command(BaseCommand):
    help = 'Check for plants that haven’t been watered for 7 days'

    def handle(self, *args, **kwargs):
        # Setup your application instead of bot for async operations
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

        async def send_async_message(chat_id, text):
            await application.bot.send_message(chat_id=chat_id, text=text)

        threshold_date = timezone.now() - timedelta(days=7)
        watered_plants = WaterLog.objects.values('plant_name').annotate(latest_watering=Max('watered_at')).filter(
            latest_watering__lte=threshold_date)

        loop = asyncio.get_event_loop()
        for plant in watered_plants:
            message = f"Plant {plant['plant_name']} hasn't been watered for 7 days!"
            loop.run_until_complete(send_async_message(chat_id=TELEGRAM_CHAT_ID, text=message))
            self.stdout.write(self.style.WARNING(message))