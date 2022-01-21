from django.contrib import messages
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from operators.forms import RegisterOperator
from ticket.models import ticket
from busrun.models import ordered_location_table,busrun
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import user_passes_test

def manage(request):
    if request.POST:
        form = RegisterOperator(request.POST)
        if form.is_valid():
            form.save()
            _username = form.cleaned_data.get('username')
            user = User.objects.get(username=_username)
            group = Group.objects.get(name="operator")
            user.groups.add(group)
            messages.success(request, f'Bus Operator {_username} has been created!')
            return redirect("operator-manage")        
    else:
        form = RegisterOperator()
    return render(request, 'operator/operator.html', {
        'form':form,
        'operators':User.objects.filter(groups__name="operator")
    })

def scan(request):
    return render(request,"operator/scanQrCode.html")
    
def delete(request, operator_id):
    if request.method == "DELETE":
        operator = User.objects.get(id=operator_id)
        operator.delete()
        return JsonResponse({'status':True, 'message':f'Operator {operator.username} has been removed'})
    else:
        return JsonResponse({'status':False, 'message':'request was not of method type delete'})

def viewTickets(request):
    bus_run_id = busrun.getBusRunId(busrun,request.user.id)
    unused_tickets = ticket.objects.filter(status="unused",bus_run_id=bus_run_id).order_by('from_location_id').values()
    scanned_tickets = ticket.objects.filter(status="scanned",bus_run_id=bus_run_id).order_by('from_location_id').values()
    all_unused_tickets = []
    all_scanned_tickets = []
    if len(unused_tickets) != 0:
        for ticket_ in unused_tickets:
            all_unused_tickets.append([ordered_location_table.get_location_name(int(ticket_['from_location_id'])),ordered_location_table.get_location_name(int(ticket_['to_location_id'])),ticket_['number_of_seats'],ticket_['status']])
    if len(scanned_tickets) != 0:
        for ticket_ in unused_tickets:
            all_scanned_tickets.append([ordered_location_table.get_location_name(int(ticket_['from_location_id'])),ordered_location_table.get_location_name(int(ticket_['to_location_id'])),ticket_['number_of_seats'],ticket_['status']])
    ticket_summary = [len(unused_tickets),len(scanned_tickets),len(scanned_tickets)+len(unused_tickets)]

    return render(request,"operator/viewTickets.html",{"all_unscanned_tickets": all_unused_tickets,"all_scanned_tickets": all_scanned_tickets,"ticket_summary": ticket_summary})
