from django import forms
from ticket.models import ticket
from busrun.models import busstop_to_busstop,busrun,location
from busrun.models import ordered_location_table as ord_table

class purchaseForm(forms.Form):
    order_table = ord_table.objects.all()
    location_list = location.objects.all()
    from_choice = [
        ["",'Select Current Location'],
    ]
    #loading all locations to the select field from database
    location_name = ""
    integer = 0
    for order in order_table:
        for location_ in location_list:
            if order.location_id == location_.id:
                integer = integer+1
                from_choice.append([order.order,location_.location_name])
                break
    to_choice = (
    ["", "Select Travel Destination"],
    )
    #WEST meaning Upper Route and East means Lower Route
    cardinalDirection = (
        ('',"Choose Direction"),
        ('WT',"West"),
        ('ET','East')
    )
    bus_choice = (
    ["", "Select Bus Type"],
    ["REG","Regular"],
    ["EXP","Express"]
    )
    _from = forms.ChoiceField(widget=forms.Select(attrs={'class': "form-select"}),choices = from_choice)
    direction = forms.ChoiceField(widget=forms.Select(attrs={'class': "form-select"}),choices= cardinalDirection)
    _to = forms.ChoiceField(widget=forms.Select(attrs={'class': "form-select"}),choices = to_choice)
    _bus_type = forms.ChoiceField(widget=forms.Select(attrs={'class': "form-select"}),choices = bus_choice)
    number_of_seats = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control"}),required=True)