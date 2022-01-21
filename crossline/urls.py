"""crossline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as authViews
from passenger import views as passengerViews
from user import views as userViews
from django.conf.urls import handler404, handler500
from crossline.lib.job import bulkCreateTickets

handler500 = userViews.handle404
handler404 = userViews.handle404
urlpatterns = [
    path('', userViews.home, name="index"),
    path('admin/', admin.site.urls),
    path('register/', passengerViews.register, name="register-passenger"),
    path('login/', authViews.LoginView.as_view(template_name="passenger/login.html", redirect_authenticated_user=True), name="login"),
    path('logout/', authViews.LogoutView.as_view(template_name='passenger/logout.html'), name="logout"),
    path('passenger/', include('passenger.urls')),
    path('operators/', include('operators.urls')),
    path('bus/', include('bus.urls')),
    path('ticket/',include('ticket.urls')),
    path('busschedule/', include('busrun.urls')),
    path('busstopstats/', include('busstop.urls')),
    path('bulkcreatetickets/', bulkCreateTickets )
]

