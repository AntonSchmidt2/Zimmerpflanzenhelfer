# waterlog/utils.py

import os
import json
from telegram import Bot, error as telegram_error
from django.conf import settings

# Load configuration
config_path = os.path.join(settings.BASE_DIR, 'config.json')
with open(config_path) as config_file:
    config = json.load(config_file)

# Initialize bot with token from configuration
bot = Bot(token=config.get('TELEGRAM_BOT_TOKEN'))

def send_notification(plant):
    try:
        message = bot.send_message(chat_id=config.get('TELEGRAM_CHAT_ID'),
                                   text=f"Plant {plant.name} hasn't been watered for 7 days!")
        return message.message_id
    except telegram_error.TelegramError as e:
        print(f"Error sending notification: {e}")
        return None

def delete_notification(water_log):
    try:
        # Delete the message using the message_id from the WaterLog instance
        bot.delete_message(chat_id=config.get('TELEGRAM_CHAT_ID'), message_id=water_log.message_id)
        # Clear the message_id as it's no longer relevant
        water_log.message_id = None
        water_log.save()
    except telegram_error.TelegramError as e:
        print(f"Error deleting notification: {e}")
