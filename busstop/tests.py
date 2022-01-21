from django import setup
from django.test import TestCase
from django.test.utils import get_unique_databases_and_mirrors
from busstop.models import get_boarding, get_deboarding, stats_for_busstop
from busstop.lib import load_stats_data

class BusStopStatsTestCase(TestCase):
    def setUp(self):
        # uses raw query to perform insert of test data
            #creates users and gruops for owner, operators and passengers
            #creates locations
            #creates busruns
            #creates bustops_to_busrun
            #creates busstops_to_busstops
            #creates tickets
        load_stats_data()
        
    def test_stats_for_nonExisting_busstop(self):
        # TC-5 step 1
        #Provide a BusStop identifier that does not exist
        #Expected: Returns status of false, and message stating that the bus stop does not exist
        print('\nmethod: test_stats_for_nonExisting_busstop() -- TC-5\n')
        print('calling method get_boarding(busrun_id=2, busstop_id=100, forDate="2021-04-09") -- busstop_id set to non existing bus stop identifier')
        boarding = get_boarding(2, 100, '2021-04-09')
        
        print('assertFalse boarding["status"]')
        self.assertFalse(boarding['status'])
        
        print('calling method get_deboarding(busrun_id=2, busstop_id = 100, forDate="2021-04-09") -- busstop_id set to non existing bus stop identifier')
        deboarding = get_deboarding(2, 100, '2021-04009')

        print('assertFalse deboarding["status"]')
        self.assertFalse(deboarding['status'])

    def test_stats_for_nonExisting_SecheduledRun(self):
        # TC-5 step 2
        #Provide an existing Bus Stop and a non existing ScheduledRun Identifier
        #Expected: Returns a status of false, and message stating that there are no BusStops for that Schedule
        print('\nmethod: test_stats_for_nonExisting_SecheduledRun() -- TC-5\n')
        print('calling method get_boarding(busrun_id=100, busstop_id=2, forDate="2021-04-09") -- busrun_id set to non existing bus stop identifier')
        boarding = get_boarding(100, 2, '2021-04-09')
        
        print('assertFalse boarding["status"]')
        self.assertFalse(boarding['status'])
        
        print('calling method get_deboarding(busrun_id=100, busstop_id = 100, forDate="2021-04-09") -- busrun_id set to non existing bus stop identifier')
        deboarding = get_deboarding(100, 2, '2021-04009')

        print('assertFalse deboarding["status"]')
        self.assertFalse(deboarding['status'])

        
    def test_boarding_stats(self):
        # TC-5 step 3.1,  3.2 and step 4
        print('\nmethod: test_boarding_stats() -- TC-5\n')
        #   4 tickets created, 4 registered passengers are boarding, and the total of seats being
        #   used amounts to 7
        print("calling method get_boarding(2, 13,'2021-04-09')")
        boarding = get_boarding(2, 13,'2021-04-09')
        
        print('assert boarding["seatCount"] == 7')
        self.assertEqual(boarding["seatCount"],7,)
        
        print('assert len(boarding["passengers"]) == 4')
        self.assertEqual(len(boarding["passengers"]),4,)       
        
        #Testing random existing busstop and scheduled run, should return 0 boarding
        print("calling method get_boarding(1, 2,'2021-04-09'), passing random existing busstop and busrun")
        boarding = get_boarding(1, 2,'2021-04-09')
        
        print('assert boarding["seatCount"] == 0')
        self.assertEqual(boarding['seatCount'], 0)
        
        print('assert len(boarding["passengers"]) == 0')
        self.assertEqual(len(boarding['passengers']), 0)

    def test_deboarding_seats(self):
        # TC-5 step 3.1 and 3.2 extended
        print("\nmethod: test_deboarding_seats() -- TC-5\n")
                
        # from 4 tickets created, 2 registered passengers will deboard at the provided date
        # a total of 3 seats will be freed up
        print("calling method get_deboarding(2,12,'2021-04-09')")
        debaording = get_deboarding(2,12,'2021-04-09')
        
        print("assert debaording['seatCount'] == 3")
        self.assertEqual(debaording["seatCount"], 3)
        
        print("assert len(debaording['passengers']) == 2")
        self.assertEqual(len(debaording["passengers"]), 2)

    def test_stats_for_busstop(self):
        # combined test, between boarding and deboarding
        print('\nmethod: test_stats_for_busstop() -- TC-5 combined test\n')
        print('calling method stats_for_busstop(2, 13, "2021-04-09")')
        stats = stats_for_busstop(2, 13, '2021-04-09')
        
        print("assert len(stats['boarding']['passengers']) == 4")
        self.assertEqual(len(stats['boarding']['passengers']), 4)
        
        print("assert len(stats['deboarding']['passengers']) == 0\n")
        self.assertEqual(len(stats['deboarding']['passengers']), 0)
