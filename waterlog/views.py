from django.http import JsonResponse
from django.shortcuts import redirect
from django.db import IntegrityError
from .models import WaterLog

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import IntegrityError
from .models import Plant, WaterLog

def log_watering(request):
    plant_name = request.GET.get('plant_name', '')
    if plant_name:
        plant, created = Plant.objects.get_or_create(name=plant_name)
        WaterLog.objects.create(plant=plant, watered_at=datetime.now())
        return JsonResponse({'status': 'success', 'message': f'{plant_name} watered successfully'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Plant name is required'}, status=400)

def show_logs(request):
    logs = WaterLog.objects.all().order_by('-watered_at')
    return render(request, 'waterlog/logs.html', {'logs': logs})

def log_page(request):
    plants = Plant.objects.all()
    context = {'plant_list': plants}
    return render(request, 'waterlog/manual_log.html', context)

def add_manual_log(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        plant_name = request.POST.get('plant_name')
        watered_at = request.POST.get('watered_at')

        if action == 'log_existing':
            plant = Plant.objects.get(name=plant_name)
            WaterLog.objects.create(plant=plant, watered_at=watered_at)
        elif action == "log_new":
            plant = Plant.objects.create(name=plant_name)
            WaterLog.objects.create(plant=plant, watered_at=watered_at)

        return redirect('waterlog:show_logs')
