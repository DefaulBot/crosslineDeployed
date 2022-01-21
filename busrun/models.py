from django.db import models
from django.utils.translation import gettext_lazy as _
from bus.models import Bus
from datetime import datetime,timedelta
import requests
import math
from django.contrib.auth.models import User

# Unsorted table of all locations from Terminal A to terminal B
class location(models.Model):
    location_name = models.CharField(max_length=80)
    longitude = models.CharField(max_length=20)
    latitude = models.CharField(max_length=15)
    
    def get_location_(self,location_id):
        location_ = self.objects.filter(id=location_id).values()
        print("locaition: ",location_)
        return location_[0]['id']

#Contains a sorted table of location from Terminal A to Terminal B
class ordered_location_table(models.Model):
    location = models.ForeignKey(location,models.SET_NULL,blank=True,null=True)
    order = models.IntegerField()

    def get_buses(self,bus_choice,direction,from_loc,to_loc):
        #getting all busruns relating to the user bus choice
        order_locaction_list = self.objects.all()
        bus_run = busrun.objects.filter(run_type=bus_choice).values()
        buses = []
        buses_through_destination = []
        for bus in bus_run:
            dep_order = self.find_order(self,bus['departure_location_id'])
            #getting the busrun of the buses according to the direction of where the user is going 
            if dep_order > to_loc and direction == "WT":
                buses.append(bus)
            elif dep_order < to_loc and direction == "ET":
                buses.append(bus)

        user_to_loc_order = to_loc
        
        #check to see if user is going to a location within the bus route      
        for bus in buses:
            # !compare the current time with the time of the bus departure before adding the bus to a list and displaying it to the user
            if direction == 'WT' and self.find_order(self,bus['destination_location_id']) <= user_to_loc_order:# and current time is < time taken from bus departure to user location
                #bug [what if the user is departuring from the bus departure location]
                dt = datetime(2009, 12, 2, 6, 12, 0, 0)#datetime.now()
                comparison = self.compareTime(self,dt,bus['departure_time'],self.get_location_duration(bus['departure_location_id'],self.find_location_with_order(self,to_loc)))
                #checks if there are buses that have not passed the user location and that are passing through user location
                if  comparison[1]== True:
                    buses_through_destination.append([bus,comparison[0]])
            elif direction == 'ET' and self.find_order(self,bus['destination_location_id']) >= user_to_loc_order:
                comparison = self.compareTime(self,dt,bus['departure_time'],self.get_location_duration(bus['departure_location_id'],self.find_location_with_order(self,to_loc)))
                #checks if there are buses that have not passed the user location and that are passing through user location
                if comparison[1] == True:
                    buses_through_destination.append([bus,comparison[0]])
        if len(buses_through_destination) == 0:
            print()
            print("BUSES THROUGH DESTINATION IS EMPTY")
            print()
            print(buses_through_destination)
            return "empty"
        return buses_through_destination #try to return a array of the  bus that the user can pruchase a ticket for and the time of arrival to user location for each bus
    #adds duration to current time and
    def compareTime(self,current_time,departure_time,duration):
        #get time of departure of bus and compare it with a estimate calculation of arrival time
        duration = math.floor((math.floor(duration)/60))
        
        #calculating the time that the bus will arrive at user destination
        time_to_user_location = datetime(year=2021, month=11, day=23,hour=departure_time.hour,minute=departure_time.minute) + timedelta(minutes=duration)
        if current_time.time() < time_to_user_location.time():
            return [time_to_user_location.time(),True]
        elif current_time.time() > time_to_user_location.time():
            return [0,False]
        return [0,False]
    
    def find_location_with_order(self,location_order):
        location_ = self.objects.filter(order=location_order).values()
        return location_[0]['location_id']
        
    def get_location_name(location_id):
        location_name = location.objects.filter(id=location_id).values('location_name')
        return location_name[0]['location_name']

    def find_order(self,location_id):
        location_ = list(self.objects.filter(location_id=location_id).values())
        return location_[0]['order']

    def add_delta(tme, delta):
        # transform to a full datetime first
        return (datetime.datetime.combine(datetime.date.today(), tme) + 
                delta).time()

    def get_location_duration(from_location,to_location):

        from_loc = location.objects.filter(id=from_location).values()
        to_loc = location.objects.filter(id=to_location).values()
        #longitude: -,latitude: + ; longitude: -,latitude: +
        r = requests.get("https://api.mapbox.com/directions/v5/mapbox/driving/"+from_loc[0]['longitude']+","+from_loc[0]['latitude']+";"+to_loc[0]['longitude']+","+to_loc[0]['latitude']+"?access_token=pk.eyJ1IjoiZmVocmYiLCJhIjoiY2s5MjF4a3dyMDJtODNrazJ1ejgzNHVyOSJ9.TZ_pbUvRg96kTugiyhUgWg")
        r_py = r.json()
        return r_py['routes'][0]['duration']

    def get_locations_count(self,from_location,to_location):
        qry = self.objects.filter(order__gte=to_location).exclude(order__gte=from_location).values()
        return len(qry)

class busrun(models.Model):
    class BusTypes(models.TextChoices):
        EXPRESS = 'EXP', _('express')
        REGULAR = 'REG', _('regular')
    run_type = models.CharField(max_length=3, choices=BusTypes.choices, default=BusTypes.REGULAR)
    bus = models.ForeignKey(Bus,on_delete=models.DO_NOTHING,)
    departure_location = models.ForeignKey(location,blank=True,null=True,on_delete=models.DO_NOTHING,related_name="departure_location",)
    destination_location = models.ForeignKey(location,blank=True,null=True,on_delete=models.DO_NOTHING,related_name="destination_location",)
    departure_time = models.TimeField()
    
    def getRange(self):
        if self.departure_location.id > self.destination_location.id:
            return (self.destination_location.id, self.departure_location.id)
        return (self.departure_location.id, self.destination_location.id)
    
    def orderLocation(self):
        if self.departure_location.id > self.destination_location.id:
            return '-id'
        return 'id'

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
    
    def getBusRunId(self,operator_id):
        operator_bus_id = Bus.objects.filter(conductor_id=operator_id).values()[0]['id']
        return self.objects.filter(bus_id=operator_bus_id).values()[0]['id']

    def getBusStopsForBusRun(id):
        busrn = busrun.objects.get(id=id)
        location_to = busrn.destination_location.longitude
        location_from = busrn.departure_location.longitude
        locations = []

        if location_to < location_from:
            locations = location.objects.filter(longitude__range=(location_from, location_to)).order_by('-longitude')
        else:
            locations = location.objects.filter(longitude__range=(location_from, location_to)).order_by('longitude')
        
        return locations

# The user stop within the bus run from bus terminal A to Terminal B
class busstop_in_busrun(models.Model):
    bus_run = models.ForeignKey(busrun,on_delete=models.DO_NOTHING)
    location = models.ForeignKey(location,blank=True,null=True,on_delete=models.DO_NOTHING,related_name="busstop_location_id")
    
    def bulkInsert(data, run_id):
        busRun = busrun.objects.get(id=run_id)
        for i in range(len(data["locations"])):
            loc = location.objects.get(id=data["locations"][i])
            busstop_in_busrun.objects.create(bus_run=busRun, location=loc)

class busstop_to_busstop(models.Model):
    bus_run = models.ForeignKey(busrun,on_delete=models.CASCADE)
    from_location = models.ForeignKey(location,models.SET_NULL,blank=True,null=True,related_name="from_location_id",)
    to_location = models.ForeignKey(location,models.SET_NULL,blank=True,null=True,related_name="to_location_id",)
    bus_fair = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return "Testing %s, %s, %s,%s," % (self.bus_run_id,self.from_location_id,self.to_location_id,self.bus_fair)

    def get_busstop_info(self,from_loc,to_loc):
        run_lst = self.objects.filter(from_location=from_loc,to_location=to_loc).values()
        print(run_lst)
        for run in run_lst:
            print("found")
            return run
        return 0
        
    def generateData(busrun_id):
        busstops = busstop_in_busrun.objects.filter(bus_run_id=busrun_id)
        for i in range(len(busstops)-1):
            for x in range(i+1, len(busstops)):
                busstop_to_busstop.objects.create(
                    bus_run = busstops[i].bus_run, 
                    from_location = busstops[i].location,
                    to_location = busstops[x].location,
                    bus_fair = 4.00
                )
