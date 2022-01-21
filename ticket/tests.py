from busstop.lib import load_stats_data
from django.test import TestCase
from ticket.models import ticket
from django.contrib.auth.models import User
from busrun.models import busstop_to_busstop,busrun,location
from bus.models import Bus
from django.db import models
from datetime import datetime

class purchaseTicketTestCase(TestCase):
    def setUp(self):
        #load test data
        load_stats_data()
        #creating new user
        User.objects.create(is_superuser=1,email="fehrfaber@gmail.com",password="123",first_name="default",last_name="default2",is_active=1,username=f"john{datetime.now()}",is_staff=1)
    
    def test_purchaseTicket(self):
        print('\nmethod: test_purchaseTicket() -- TC-1\n')
        user = User.objects.get(email="fehrfaber@gmail.com")
        #creating new bus instance
        bus = Bus.objects.create(plate_number="2514-5542",name="James",capacity=30,driver=user,conductor=user)
        #bus = Bus.objects.get(id=1)

        #creating new location instance
        location_ = location.objects.create(location_name="Belize",latitude="-88.218672",longitude="-88.218672")
        #location_ = location.objects.get(id=1)

        #creating new busrun instance
        busrun_ins = busrun.objects.create(run_type="EXP",bus=bus,departure_location=location_,destination_location=location_,departure_time="7:00:00")
        #busrun_ins = busrun.objects.get(id=1)

        #creating busstop_to_busstop instance
        b_to_b = busstop_to_busstop.objects.create(bus_run=busrun_ins,from_location=location_,to_location=location_,bus_fair=2.50)
        #b_to_b = busstop_to_busstop.objects.get(id=1)
        
        #creating new ticket
        obj1 = ticket.objects.create(passenger_id=user,busstop_to_busstop_id=b_to_b,status="unused",number_of_seats=8,QRcode="help",expiration_date="2021-04-06",price=2.50,purchase_date="2021-04-06")
        ticket.objects.create(passenger_id=user,busstop_to_busstop_id=b_to_b,status="used",number_of_seats=8,QRcode="help",expiration_date="2021-04-06",price=2.60,purchase_date="2021-04-06")

        #obj1 = ticket.objects.filter(id=1)
        print(obj1)
        status_= "unused"
        number_of_seats = 4
        
        print("Asserting if ticket status is unused")
        self.assertEqual(status_,"unused")
        print("Asserting if number of seats is less than capacity")
        self.assertTrue(number_of_seats < 40)

    def test_cancelTicket(self):
        user = User.objects.create(is_superuser=1,email="fehrfaber@gmail.com",password="123",first_name="default",last_name="default2",is_active=1,username=f"John{datetime.now()}",is_staff=1)
        #user = User.objects.get(id=2)
        #creating new bus instance
        bus = Bus.objects.create(plate_number="2514-5542",name="James",capacity=30,driver=user,conductor=user)
        #bus = Bus.objects.get(id=1)

        #creating new location instance
        location_ = location.objects.create(location_name="Belize",latitude="-88.218672",longitude="-88.218672")
        #location_ = location.objects.get(id=2)

        #creating new busrun instance
        busrun_ins = busrun.objects.create(run_type="EXP",bus=bus,departure_location=location_,destination_location=location_,departure_time="8:00:00")
        #busrun_ins = busrun.objects.get(id=2)

        #creating busstop_to_busstop instance
        b_to_b = busstop_to_busstop.objects.create(bus_run=busrun_ins,from_location=location_,to_location=location_,bus_fair=2.50)
        #b_to_b = busstop_to_busstop.objects.get(id=2)

        ticket_to_cancel = ticket.objects.create(passenger_id=user,busstop_to_busstop_id=b_to_b,status="unused",number_of_seats=8,QRcode="help",expiration_date="2021-04-06",price=2.50,purchase_date="2021-04-06")
        #ticket_to_cancel = ticket.objects.get(id=1)
        ticket_to_cancel.status = "canceled"
        ticket_to_cancel.save()
        self.assertEqual(ticket_to_cancel.status,"canceled")


    '''
    Testing for validate_ticket() below 
    '''
    def test_validate_ticket_for_mode_boarding(self):
        
        # TC-3 step 1
        print('\nmethod: test_validate_ticket_for_mode_boarding() TC-3\n')
        tckt = ticket.objects.get(id=1)
        
        print('calling method tckt.validate_ticket(busrun_id=2, mode="boarding") -- ticket status unused, currently scheduled run')
        is_valid = tckt.validate_ticket(2, 'boarding')

        print('assertTrue is_valid["status"]')
        self.assertTrue(is_valid['status'])

        #TC-3 step 2
        print('calling method tckt.validate_ticket(busrun_id=100, mode="boarding") -- not currently scheduled run')
        is_valid = tckt.validate_ticket(100, 'boarding')

        print('assertFalse is_valid["status"]')
        self.assertFalse(is_valid['status'])
        
        #TC-3 step 3
        tckt.status = 'canceled'
        print('calling method tckt.validate_ticket(busrun_id=2, mode="boarding") -- ticket status canceled')
        is_valid = tckt.validate_ticket(2, 'boarding')

        print('assertFalse is_valid["status"]')
        self.assertFalse(is_valid['status'])

        #TC-3 step 5
        tckt.status = 'in use'
        print('calling method tckt.validate_ticket(busrun_id=2, mode="boarding") -- ticket status "in use"')
        is_valid = tckt.validate_ticket(2, 'boarding')

        print('assertFalse is_valid["status"]')
        self.assertFalse(is_valid['status'])

        
        #TC-3 step 7
        tckt.status = 'used'
        print('calling method tckt.validate_ticket(busrun_id=2, mode="boarding") -- ticket status used')
        is_valid = tckt.validate_ticket(2, 'boarding')

        print('assertFalse is_valid["status"]')
        self.assertFalse(is_valid['status'])

        #TC-3 step 9
        tckt.status = 'expired'
        print('calling method tckt.validate_ticket(busrun_id=2, mode="boarding") -- ticket status expired')
        is_valid = tckt.validate_ticket(2, 'boarding')

        print('assertFalse is_valid["status"]')
        self.assertFalse(is_valid['status'])

        #TC-3 step 11
        tckt.status = 'linslie'
        print('calling method tckt.validate_ticket(busrun_id=2, mode="boarding") -- ticket status set to random string')
        is_valid = tckt.validate_ticket(2, 'boarding')

        print('assertFalse is_valid["status"]')
        self.assertFalse(is_valid['status'])

    def test_validate_ticket_for_mode_deboarding(self):
        
        print('\nmethod: test_validate_ticket_for_mode_deboarding() TC-4\n')
        tckt = ticket.objects.get(id=1)
        
        # TC-4 step 1
        tckt.status = 'unused'
        print('calling method tckt.validate_ticket(busrun_id=2, mode="deboarding") -- ticket status unused, currently scheduled run')
        is_valid = tckt.validate_ticket(2, 'deboarding')

        print('assertFalse is_valid["status"]')
        self.assertFalse(is_valid['status'])
        
        #TC-4 step 2
        tckt.status = 'canceled'
        print('calling method tckt.validate_ticket(busrun_id=2, mode="deboarding") -- ticket status canceled')
        is_valid = tckt.validate_ticket(2, 'deboarding')

        print('assertFalse is_valid["status"]')
        self.assertFalse(is_valid['status'])

        

        #TC-4 step 3
        tckt.status = 'in use'
        print('calling method tckt.validate_ticket(busrun_id=2, mode="deboarding") -- ticket status "in use"')
        is_valid = tckt.validate_ticket(2, 'deboarding')

        print('assertTrue is_valid["status"]')
        self.assertTrue(is_valid['status'])

        
        #TC-4 step 4
        tckt.status = 'used'
        print('calling method tckt.validate_ticket(busrun_id=2, mode="deboarding") -- ticket status used')
        is_valid = tckt.validate_ticket(2, 'deboarding')

        print('assertFalse is_valid["status"]')
        self.assertFalse(is_valid['status'])

        #TC-4 step 5
        tckt.status = 'expired'
        print('calling method tckt.validate_ticket(busrun_id=2, mode="deboarding") -- ticket status expired')
        is_valid = tckt.validate_ticket(2, 'deboarding')

        print('assertFalse is_valid["status"]')
        self.assertFalse(is_valid['status'])

        #TC-4 step 6
        tckt.status = 'linslie'
        print('calling method tckt.validate_ticket(busrun_id=2, mode="deboarding") -- ticket status set to random string')
        is_valid = tckt.validate_ticket(2, 'deboarding')

        print('assertFalse is_valid["status"]')
        self.assertFalse(is_valid['status'])
