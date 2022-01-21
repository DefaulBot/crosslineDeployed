from ticket.models import ticket
from busrun.models import busrun, busstop_in_busrun, busstop_to_busstop
from django.db import models
from datetime import datetime
# Create your models here.

def parse2DArray(arr):
    seatCountBoarding = 0
    passengers = []
    for i in range(len(arr)):
        for x in range(len(arr[i])):
            seatCountBoarding += arr[i][x].number_of_seats
            passengers.append(arr[i][x].passenger_id)    
    return {'status': True, 'seatCount':seatCountBoarding, 'passengers':passengers}

def exists(busrun_id, busstop_id):
    #check if the bus run exists
    busstops_in_busrun_ = busstop_in_busrun.objects.filter(bus_run_id = busrun_id)
    if not busstops_in_busrun_.count() > 0:
        return {'status': False, 'message':f'bus run {busrun_id} does not exist'}
    #check if the busstop exists in the bus run
    busstop_ = busstop_in_busrun.objects.filter(bus_run_id=busrun_id, location_id=busstop_id)
    if not busstop_.count() > 0:
        return {'status':False, 'message':f'bus stop {busstop_id} does not exist for the bus run {busrun_id}'}

    return {'status': True}

def get_boarding(busrun_id, busstopid, forDate=datetime.today()):
    
    doesExists = exists(busrun_id, busstopid)
    if not doesExists['status']:
        return doesExists

    btb = busstop_to_busstop.objects.filter(bus_run_id=busrun_id, from_location_id=busstopid)
    tickets = []
    for b in btb:
        tcks = ticket.objects.filter(busstop_to_busstop_id = b.id, expiration_date=forDate, status="unused")
        if len(tcks)!=0:
            tickets.append(tcks)   
    
    return parse2DArray(tickets)

def get_deboarding(busrun_id, busstopid, forDate=datetime.today()):
    doesExists = exists(busrun_id, busstopid)
    if not doesExists['status']:
        return doesExists
    
    btb = busstop_to_busstop.objects.filter(bus_run_id=busrun_id, to_location_id=busstopid)
    tickets = []
    for b in btb:
        tcks = ticket.objects.filter(busstop_to_busstop_id = b.id, expiration_date=forDate)
        if len(tcks)!=0:
            tickets.append(tcks)   
    
    return parse2DArray(tickets)

def stats_for_busstop(busrun_id, busstopid, forDate=datetime.today()):
    return {
        'deboarding':get_deboarding(busrun_id, busstopid, forDate),
        'boarding':get_boarding(busrun_id, busstopid, forDate)
    }