from django.db import models
from busrun.models import busrun, busstop_to_busstop,location
from django.contrib.auth.models import User, Group
import datetime
from decimal import Decimal
# Create your models here.
class ticket(models.Model):
    passenger = models.ForeignKey(User,models.SET_NULL,blank=True,null=True,)
    from_location = models.ForeignKey(location,on_delete=models.DO_NOTHING,blank=True,null=True,related_name="from_location")
    to_location = models.ForeignKey(location,on_delete=models.DO_NOTHING,blank=True,null=True,related_name="to_location")
    bus_run = models.ForeignKey(busrun,on_delete=models.DO_NOTHING,blank=True,null=True,related_name="bus_run")
    status = models.CharField(max_length=15)
    number_of_seats = models.IntegerField(default=35)
    QRcode = models.TextField()
    expiration_date = models.DateTimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)
    
    def createMessage(self, status, message=None):
        return {'status':status, 'message':message}

    def calculate_price(from_loc,to_loc):
        return 0
    
    def validate_ticket(self, busrun_id, mode='boarding'):
        #check if the mode is set to boarding and the ticket status is unused    
        if mode == 'boarding' and self.status == 'unused':
            # check if the ticket belongs to the current scheduled run
            if self.busstop_to_busstop_id.bus_run.id == busrun_id:
                return self.createMessage(True)
            return self.createMessage(False, f'the ticket is not for the current bus run, ticket is for {self.busstop_to_busstop_id.bus_run.departure_time} run')

        #check if the mode is set to deboarding and the ticket status is set to 'in use'
        elif mode == 'deboarding' and self.status == 'in use': 
            #check if the ticket belongs to the current scheduled bus run
            if self.busstop_to_busstop_id.bus_run.id == busrun_id:
                return self.createMessage(True)
            return self.createMessage(False, f'the ticket is not for the current bus run, ticket is for {self.busstop_to_busstop_id.bus_run.departure_time} run')

        return self.createMessage(False, f'scan mode is set to {mode} but status is {self.status}')

    def get_ticket_by_qrcode(self,qrcode):
        return ticket.objects.get(QRcode= qrcode) 
class passenger_credit(models.Model):
    passenger = models.ForeignKey(User,models.SET_NULL,blank=True,null=True,)
    credit_amount = models.DecimalField(max_digits=20, decimal_places=2)
    
    def calculate_price(self,p_id,price):
        
        user_creds = self.objects.filter(passenger_id=p_id).values()   
        print("cred length: ",user_creds)  
        if len(user_creds) == 0:
            user_credits = 0
            return "Insufficient Funds. Please Recharge your funds."
        else:
            user_credits = user_creds[0]['credit_amount']
            print("cred amount: ",user_credits)
            user_credits = user_credits - Decimal(price)
            self.objects.filter(passenger_id=p_id).update(credit_amount=user_credits)
            return "success"
            
    def get_credits(self,user_id):
        user_creds = self.objects.filter(passenger_id=user_id).values()
        return user_creds[0]['credit_amount']