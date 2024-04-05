from django.utils import timezone  # Corrected import for timezone
from django.http import JsonResponse
from .models import Plant, WaterLog
from .utils import delete_notification
from django.shortcuts import render


def log_watering(request):
    # Get 'plant_name' from query parameters
    plant_name = request.GET.get('plant_name', None)

    if not plant_name:
        return JsonResponse({'status': 'error', 'message': 'Plant name is required'}, status=400)

    # Attempt to retrieve the plant by name
    try:
        plant = Plant.objects.get(name=plant_name)
    except Plant.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Plant not found'}, status=404)

    # Create a WaterLog instance for the plant
    WaterLog.objects.create(plant=plant, watered_at=timezone.now())

    # If there's a message ID, attempt to delete the Telegram message
    # Assuming each WaterLog instance has a `message_id` and not the Plant model itself
    # The following logic might need to be adjusted based on your actual model structure
    latest_water_log = WaterLog.objects.filter(plant=plant).latest('watered_at')
    if latest_water_log.message_id:
        delete_notification(latest_water_log)

    return JsonResponse({'status': 'success', 'message': f'{plant.name} watered successfully'})


def show_logs(request):
    logs = WaterLog.objects.all().order_by('-watered_at')
    return render(request, 'waterlog/logs.html', {'logs': logs})
