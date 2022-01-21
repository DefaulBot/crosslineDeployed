from bus.models import Bus
from django import forms
from django.contrib.auth.models import User

class CreateBus(forms.ModelForm):
    
    class Meta:
        model = Bus
        fields = ['name', 'capacity', 'plate_number', 'driver', 'conductor']

    def __init__(self, *args, **kwargs):
        super(CreateBus, self).__init__(*args, **kwargs)

        if self.instance:
            operators = User.objects.filter(groups__name="operator")
            self.fields['driver'].queryset = operators
            self.fields['conductor'].queryset = operators
            