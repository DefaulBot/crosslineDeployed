from django.shortcuts import redirect, render

from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    grp = request.user.groups.values_list('name',flat=True).first()
    if grp == 'passenger':
        return redirect(f'/passenger/')
    else:
        return render(request,'manage/home.html')



def handle404(request, *args, **kwargs):
    return redirect('/')
