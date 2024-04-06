from django.http import JsonResponse
from django.shortcuts import redirect
from django.db import IntegrityError
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


def log_page(request):
    # print only distinct plant names
    plant_list = WaterLog.objects.values_list('plant_name', flat=True).distinct()
    context = {'plant_list': plant_list}
    return render(request, 'waterlog/manual_log.html', context)


def add_manual_log(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        watering_info = dict(request.POST)
        del watering_info['csrfmiddlewaretoken']
        # 'plant-name': ['PlantName'], 'watered-at': ['2024-04-05']}
        log_input = {i:j[0] for i, j in watering_info.items()}
        print(log_input)
        # {'plant-name': 'PlantName', 'watered-at': '2024-04-05'}
        if action == 'log_existing':
            # plant_info = WaterLog.objects.get(plant_name=input['plant-name'])
            # plant_info.watered_at = input['watered-at']
            name = log_input['plant-name']
            watered = log_input['watered-at']
        elif action == "log_new":
            name = log_input['name']
            watered = log_input['new_watered']

        try:
            plant_info = WaterLog.objects.create(
                plant_name=name,
                watered_at=watered
            )
            plant_info.save()
        except IntegrityError:
            pass

        return redirect('waterlog:show_logs')

