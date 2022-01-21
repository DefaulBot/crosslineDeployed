from django.shortcuts import redirect, render
from passenger.forms import RegisterPassenger
from django.contrib.auth.models import User, Group
from django.contrib import messages


# Create your views here.
def register(request):
    if request.POST:
        form = RegisterPassenger(request.POST)
        if form.is_valid():
            form.save()
            _username = form.cleaned_data.get('username')
            user = User.objects.get(username=_username)
            group = Group.objects.get(name="passenger")
            user.groups.add(group)
            messages.success(request, f'You have been registered successfully!')
            return redirect("login")        
    else:
        form = RegisterPassenger()
    return render(request, 'passenger/register.html', {
        'form':form,
    })

def login(request):
    return render(request, "passenger/login.html")

def home(request,):
    grp = request.user.groups.values_list('name', flat=True).first()    
    if grp == 'passenger':
        return render(request, "passenger/home.html")
    else:
        return redirect('index') 