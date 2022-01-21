from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from django import forms
from .forms import purchaseForm
from bus.models import Bus
from ticket.models import ticket,passenger_credit
from django.contrib.auth.models import User
from busrun.models import busrun,busstop_to_busstop,ordered_location_table,location
from datetime import datetime,timedelta
import math
import os
import qrcode
from PIL import Image
import base64
from io import BytesIO
from decimal import Decimal

def purchaseTicket(request):
    err_message =  ""
    if request.method == 'POST':
        current_user = request.user
        form = purchaseForm(request.POST)
        #accepting post values from purchaseticket.html
        _to = int(form.data['_to']) # needs to be translated to reference location
        _from = int(form.data['_from']) # needs to be translated to reference location
        bus_choice = form.data['_bus_type']
        direction = form.data['direction']
        number_of_seats = int(form.data['number_of_seats'])

        # application generated data
        ticket_status = "unused"
        expiration_date = "2007-10-04"
        QRcode = "1location"
        purchase_date = "2007-10-04"

        #the queries needs validations

        bus_run = ordered_location_table.get_buses(ordered_location_table,bus_choice,direction,_from,_to)
        
        if bus_run == "empty":
            err_message = "none"
            form = purchaseForm()
            username = request.user.username
            buses = []
            return render(request, 'ticket/purchaseticket.html',{'form':form,'username': username,'err_msg':err_message,'available_buses': buses})
        tickets = []
        buses = []
        qry = []
        price = 0
        user_to_from = str(_to)+','+str(_from)
        user_ticket = ticket.objects.filter(passenger_id=request.user.id).values()

        for UT in user_ticket:
            if UT['status'] == "unused" or UT['status'] == "scanned":
                err_message = "You have one ticket active. Please cancel before making another purchase."
                form = purchaseForm()
                username = request.user.username
                number_of_seats = 0
                return render(request, 'ticket/purchaseticket.html',{'form':form,'username': username,'err_msg':err_message,'available_buses': buses,'number_of_seats': number_of_seats})

        for bus in bus_run:
            tickets = ticket.objects.filter(bus_run_id = bus[0]['id']).values()
            if len(tickets) == 0 or len(tickets) < 40:
                dp_name = ordered_location_table.get_location_name(bus[0]['departure_location_id'])
                
                ds_name = ordered_location_table.get_location_name(bus[0]['destination_location_id'])
                
                duration = ordered_location_table.get_location_duration(bus[0]['departure_location_id'],ordered_location_table.find_location_with_order(ordered_location_table,_from))
                
                duration = math.floor((math.floor(duration)/60))
                time_to_user_location = datetime(year=2021, month=11, day=23,hour=bus[0]['departure_time'].hour,minute=bus[0]['departure_time'].minute) + timedelta(minutes=duration)
                time_to_user_location = time_to_user_location.strftime("%I:%M")
                #duration = math.floor((math.floor(duration)/60))
                #generating price
                
                route_location_count = ordered_location_table.get_locations_count(ordered_location_table,_from,_to)
                if route_location_count % 4 == 0:
                    price = (route_location_count/4) * 2.00
                    
                    if bus_choice == 'EXP':
                        price = price + 1.50
                    price = "{:.2f}".format(price)
                    
                else:
                    int_price = route_location_count // 4
                    float_price = (route_location_count % 4) * 1.50
                    price = (int_price + float_price) * number_of_seats

                    if bus_choice == 'EXP':
                        price = price + 1.50
                    price = "{:.2f}".format(price)
                    print("price PT: ", price)
                bs = [{'id':bus[0]['id'],'user_to_from':user_to_from,'number_of_seats': number_of_seats,'price': price,'run_type': bus[0]['run_type'],'dp_id':bus[0]['departure_location_id'],'dp_name':dp_name,'ds_id':bus[0]['destination_location_id'],'ds_name':ds_name,'arrival_time':time_to_user_location,'departure_time':bus[0]['departure_time'].strftime("%I:%M")}]
                buses.append(bs)
            else:
                err_message = "Bus is full."
    else:
        img = 0
        buses = []
        err_message = ""
    form = purchaseForm()
    username = request.user.username
    number_of_seats = 0
    return render(request, 'ticket/purchaseticket.html',{'form':form,'username': username,'err_msg':err_message,'available_buses': buses,'number_of_seats': number_of_seats})

def cancelTicket(request):
    #can only have one ticket at a time
    ticket_id = int(request.POST['ticket_id'])
    user_ticket = ticket.objects.filter(id=ticket_id).values()
    user_ticket_price = Decimal(user_ticket[0]['price'])
    user_creds = passenger_credit.get_credits(passenger_credit,request.user.id)
    user_creds = user_creds+user_ticket_price
    if os.path.isfile('static/userQRImg/'+request.user.username+'-ticket-qr.png'):
        os.remove('static/userQRImg/'+request.user.username+'-ticket-qr.png')

    ticket.objects.filter(id=ticket_id).update(status="cancelled") 
    passenger_credit.objects.filter(passenger_id=request.user.id).update(credit_amount=user_creds)

    # if user ticket status == scanned then return variable {scanned == 1} this allows the ui to not display cancel button
    # if user ticket is scanned and ticket status == scanned then update ticket to used

    #refunding user credits
    return render(request,'ticket/cancelticket.html')

def makeTicketPurchase(request):
    bus_run_id = int(request.POST['bus_run_id'])
    bus_run = busrun.objects.filter(id=bus_run_id).values()
    ticket_status = 'unused'
    # a QR lib to transform these texts to a qr code for passanger
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    user_to_from = request.POST['user_to_from']
    user_to_from = user_to_from.split(',',2)

    _to = int(user_to_from[0])
    _from = int(user_to_from[1])
    _to = location(location.get_location_(location,ordered_location_table.find_location_with_order(ordered_location_table,_to)))
    _from = location(location.get_location_(location,ordered_location_table.find_location_with_order(ordered_location_table,_from)))
    price = request.POST['price']
    price = price.split('$',1)
    
    price = float(price[1])
    price = "{:.2f}".format(price)
    msg = passenger_credit.calculate_price(passenger_credit,request.user.id,price)
    print("message: ",msg)
    if msg == "success":
        inst = ticket(passenger_id= request.user.id,bus_run_id=bus_run_id,from_location=_from,to_location=_to,status=ticket_status,number_of_seats=request.POST['number_of_seats'], QRcode="notyet", expiration_date=datetime.today(),price=price,purchase_date=datetime.today())
        inst.save()

        user_ticket = ticket.objects.filter(passenger_id=request.user.id,status="unused").values()[0]['id']
        print("user ticket: ",user_ticket)

        #data will be used to generate a qrcode for the user
        data = str(request.user.username)+","+request.POST['number_of_seats']+","+str(user_ticket)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save('static/userQRImg/'+request.user.username+'-ticket-qr.png')
        image = open('static/userQRImg/'+request.user.username+'-ticket-qr.png','rb')
        img_64_encode = base64.b64encode(image.read())

        #decoding byte image to string 
        str_instance = img_64_encode.decode("utf-8")
        ticket.objects.filter(passenger_id=request.user.id,status="unused").update(QRcode=str_instance)
        #encoding string image to bytes")
        #b_string = str.encode(str_instance)
        #encoded image:")
        #img_64_decode = base64.decodebytes(b_string)
        #image_result = open('static/userQRImg/'+request.user.username+'-ticket-qr.png','wb')
        #image_result.write(img_64_decode)
        return JsonResponse({'ERROR_MESSAGE': "success"}, status=200)
    else:
        return JsonResponse({'ERROR_MESSAGE': msg}, status=200)

def getLocation(request):
    orderT_order_id = int(request.POST['location_id'])

    direction = request.POST['direction']
    
    #getting all locations from table ordered by order field
    ordered_list = ordered_location_table.objects.all().order_by('order')
            
    #getting all locations greater or less (or not applicable)than selected location
    location_list = []
    if direction == 'WT':
        for ordered_item in ordered_list:
            if ordered_item.order < orderT_order_id:
                location_table_list = location.objects.all()
                for location_ in location_table_list:
                    if location_.id == ordered_item.location_id:
                        location_name = location_.location_name
                        location_list.append([ordered_item.order,location_name])
                        break 
    elif direction == 'ET':
        for ordered_item in ordered_list:
            if ordered_item.order > orderT_order_id:
                location_table_list = location.objects.all()
                for location_ in location_table_list:
                    if location_.id == ordered_item.location_id:
                        location_name = location_.location_name
                        location_list.append([ordered_item.order,location_name])
                        break
    else:
        location_table_list = location.objects.all()
        for ordered_item in ordered_list:
            for location_ in location_table_list:
                if location_.id == ordered_item.location_id:
                    location_name = location_.location_name
                    location_list.append([ordered_item.order,location_name])
                    break
    return JsonResponse({'location_list': location_list}, status=200)

def generateQR(request):
    seats = 0
    from_location = 0
    to_location = 0
    ticket_id = -1
    
    user_ticket = ticket.objects.filter(passenger_id=request.user.id,status="unused").values()
    user_ticket_scanned = ticket.objects.filter(passenger_id=request.user.id,status="scanned").values()
    status = 0
    departure_time = 0
    if len(user_ticket) != 0 or len(user_ticket_scanned) != 0:
        if len(user_ticket) != 0:
            from_location = user_ticket[0]['from_location_id']
            to_location = user_ticket[0]['to_location_id']
            from_location = ordered_location_table.get_location_name(from_location)
            to_location = ordered_location_table.get_location_name(to_location)
            seats = user_ticket[0]['number_of_seats']
            ticket_id = user_ticket[0]['id']
            bus_run_id = int(user_ticket[0]['bus_run_id'])
            departure_time = busrun.objects.filter(id=bus_run_id).values()
            departure_time = departure_time[0]['departure_time']
            departure_time = departure_time.strftime("%I:%M")
            status = 1

        if len(user_ticket_scanned) != 0:
            from_location = user_ticket_scanned[0]['from_location_id']
            to_location = user_ticket_scanned[0]['to_location_id']
            from_location = ordered_location_table.get_location_name(from_location)
            to_location = ordered_location_table.get_location_name(to_location)
            seats = user_ticket_scanned[0]['number_of_seats']
            ticket_id = user_ticket_scanned[0]['id']
            bus_run_id = int(user_ticket_scanned[0]['bus_run_id'])
            departure_time = busrun.objects.filter(id=bus_run_id).values()
            departure_time = departure_time[0]['departure_time']
            departure_time = departure_time.strftime("%I:%M")
            status = 0
    else:
            seats = 0
            from_location = 0
            to_location = 0
            ticket_id = 0
            status = 0
            departure_time = 0
            print("must load default values")
    return render(request, 'ticket/ticketQr.html',{'status':status, 'departure_time':departure_time,'username' : request.user.username,'ticket_id': ticket_id,'seats': seats,'from': from_location,'to': to_location})

# needs a user_id,busrun_id for conductors to see if user is on the correct bus run if not then display error
def scan_ticket(request):
    username = request.POST['username']
    number_of_seats = int(request.POST['number_of_seats'])
    ticket_id = int(request.POST['ticket_id'])
    print("ticket_id ",ticket_id)
    #getting the bus run the user purchased a ticket for
    user_ticket = ticket.objects.filter(id=ticket_id).values()
    bus_run_id = int(user_ticket[0]['bus_run_id'])
    user_bus_run = busrun.objects.filter(id=bus_run_id).values()
    #getting user bus
    user_bus = int(user_bus_run[0]['bus_id'])
    user_bus = Bus.objects.filter(id=user_bus).values()
    print("      ENTERED      ")
    #getting the id of the conductor
    conductor_id = int(user_bus[0]['conductor_id'])
    if request.user.id == conductor_id:
        print("      ENTERED      ",user_ticket[0])
        if user_ticket[0]['status'] == "unused":
            print("      UNUSED      ")
            ticket.objects.filter(id=ticket_id).update(status="scanned")
            return JsonResponse({'ERROR_MESSAGE': "",'status': "scanned"}, status=200)
        elif user_ticket[0]['status'] == "scanned":
            if os.path.isfile('static/userQRImg/'+request.user.username+'-ticket-qr.png'):
                print("removing image")
                os.remove('static/userQRImg/'+request.user.username+'-ticket-qr.png')
            ticket.objects.filter(id=ticket_id).update(status="used")
            return JsonResponse({'ERROR_MESSAGE': "",'status': "used"}, status=200)
    else:
        print("      SOMEERROR      ")
        return JsonResponse({'ERROR_MESSAGE': "Incorrect Bus",'status': ""}, status=200)
    return JsonResponse({'ERROR_MESSAGE': "",'status': ""}, status=200)

def is_ticketChanged(request):
    if(ticket.objects.latest('id').status == "unused"):
        return JsonResponse({'status': "unused", 'ticket_id': 0}, status=200)
    elif ticket.objects.latest('id').status == "scanned":
        return JsonResponse({'status':"scanned",'ticket_id': 0}, status=200)
    else:
        return JsonResponse({'status':"used", 'ticket_id': ticket.objects.latest('id').id}, status=200)

def ticketHistory(request):
    #getting users current ticket
    user_current_ticket = ticket.objects.filter(passenger_id=request.user.id,status="unused")
    UCUT = []
    UUT = []
    UCT = []
    if len(user_current_ticket) == 0:
        user_current_ticket = 0
        #getting all scanned tickets
        user_current_ticket = ticket.objects.filter(passenger_id=request.user.id,status="scanned")
        print("USER SCANNED TICK",user_current_ticket)
    if len(user_current_ticket) == 0:
            UCUT = 0
    else:
        user_current_ticket = user_current_ticket.values()
        for ticket_ in user_current_ticket:
            UCUT.append([ordered_location_table.get_location_name(ticket_['from_location_id']),
            ordered_location_table.get_location_name(ticket_['to_location_id']),
            ticket_['number_of_seats'],"{:.2f}".format(ticket_['price']),ticket_['purchase_date'].strftime("%m/%d/%Y, %H:%M:%S"),ticket_['status']])
            

    #getting users used tickets
    all_used_user_tickets = ticket.objects.filter(passenger_id=request.user.id,status="used")
    if len(all_used_user_tickets) == 0:
        UUT = 0
    else:
        all_used_user_tickets = all_used_user_tickets.values()
        for ticket_ in all_used_user_tickets:
            UUT.append([ordered_location_table.get_location_name(ticket_['from_location_id']),
            ordered_location_table.get_location_name(ticket_['to_location_id']),
            ticket_['number_of_seats'],"{:.2f}".format(ticket_['price']),ticket_['purchase_date'].strftime("%m/%d/%Y, %I:%M:%S"),ticket_['status']])
    #getting all scanned tickets
    all_cancelled_user_tickets = ticket.objects.filter(passenger_id=request.user.id,status="cancelled")
    if all_cancelled_user_tickets == 0:
        UCT = 0
    else:
        all_cancelled_user_tickets = all_cancelled_user_tickets.values()
        for ticket_ in all_cancelled_user_tickets:
            UCT.append([ordered_location_table.get_location_name(ticket_['from_location_id']),
            ordered_location_table.get_location_name(ticket_['to_location_id']),
            ticket_['number_of_seats'],"{:.2f}".format(ticket_['price']),ticket_['purchase_date'].strftime("%m/%d/%Y, %H:%M:%S"),ticket_['status']])
    return render(request, 'ticket/ticketHistory.html',{'user_current_ticket': UCUT,'all_used_user_tickets': UUT,'all_cancelled_user_tickets': UCT})
