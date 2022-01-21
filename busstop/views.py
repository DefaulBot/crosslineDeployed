import json
from django.http.response import JsonResponse
from django.shortcuts import render
from busrun.models import busstop_in_busrun, busstop_to_busstop, busrun, location
from busstop.models import stats_for_busstop
from django.core import serializers

def stats(request):
    
   
    
    return render(request, 'busstop/stats.html',{
        'busruns': busrun.objects.all(),
    })

def getLocationDataForBusRun(request, busrun_id):    
    try:
        locations = busrun.getBusStopsForBusRun(busrun_id)
    
        return JsonResponse({'status':True, 'data': serializers.serialize('json', locations)})
    except Exception as e:
        return JsonResponse({'status':False, 'message':f'bus run of id {busrun_id} does not exist'})

def getStatsForBusStop(request, busrun_id, busStop_id):
    pass