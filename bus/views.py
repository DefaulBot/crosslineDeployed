from django.shortcuts import redirect, render
from bus.forms import CreateBus
from django.contrib import messages
from bus.models import Bus
from django.contrib.auth.decorators import user_passes_test


@user_passes_test(lambda u: u.is_superuser)
def manage(request):
    if request.POST:
        form = CreateBus(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'New Bus has been added!')
            return redirect('manage-bus')
    else:
        form = CreateBus()
    return render(request, 'bus/bus.html', {'form':form, 'buses':Bus.objects.all()})

