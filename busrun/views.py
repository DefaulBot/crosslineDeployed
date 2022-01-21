import json
from django.core.checks.messages import Error
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from busrun.models import busstop_to_busstop, location, busrun, busstop_in_busrun
from busrun.forms import AddBusRun

def manage(request):
    if request.POST:
        form = AddBusRun(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage-busrun')
    else:
        form = AddBusRun()
    return render(request, "busrun/manage.html", {
        'locations':location.objects.all(), 
        'form':form,
        "busruns": busrun.objects.all()
    })


def createLocation(request):
    if request.body:
        unicjson = request.body.decode('utf-8')
        body = json.loads(unicjson)
        loc = location.objects.create(location_name=body["name"], longitude=body['longitude'], latitude=body["latitude"])
        return JsonResponse({'status':True, 'message':f'location {loc.location_name} created!', 'data':body})
    else:
        return JsonResponse({'status':False, 'message':'an error occurred, the request body is empty'})

def addLocation(request, busrun_id):
    if request.body:
        unicjson = request.body.decode('utf-8')
        body = json.loads(unicjson)
        busstop_in_busrun.bulkInsert(body, busrun_id)
        busstop_to_busstop.generateData(busrun_id)
        return JsonResponse({'status':True, 'message':'added busstops to busrun, generated schedule, make sure to edit the bus fair'})



    bus_run = busrun.objects.get(id=busrun_id)
    locations = location.objects.filter(id__range=bus_run.getRange()).order_by(bus_run.orderLocation())
    return render(request, 'busrun/busrun_add_locations.html',{
        "busrun":bus_run, 
        "locations":locations,
        "busstops":busstop_in_busrun.objects.filter(bus_run_id=busrun_id),        
        "busschedule":busstop_to_busstop.objects.filter(bus_run_id=busrun_id)
    })