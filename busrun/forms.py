from django import forms
from django.forms import fields
from busrun.models import busrun


class AddBusRun(forms.ModelForm):
    departure_time = forms.TimeField(
        required=True,
        input_formats=['%H:%M:%S'],
        widget=forms.TimeInput(attrs={'class':'form-control'}), 
        error_messages={"required":"This field is required"}
    )
    
    class Meta:
        model = busrun
        fields = [
            'run_type', 
            'bus',
            'departure_time', 
            'departure_location', 
            'destination_location'
        ]