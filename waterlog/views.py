from django.http import JsonResponse
from .models import WaterLog

def log_watering(request):
    plant_name = request.GET.get('plant_name', '')
    if plant_name:
        WaterLog.objects.create(plant_name=plant_name)
        return JsonResponse({'status': 'success', 'message': f'{plant_name} watered successfully'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Plant name is required'}, status=400)


from django.shortcuts import render

def show_logs(request):
    logs = WaterLog.objects.all().order_by('-watered_at')
    return render(request, 'waterlog/logs.html', {'logs': logs})
