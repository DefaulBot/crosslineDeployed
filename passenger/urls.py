import passenger
from django.urls import path
import passenger.views as passengerViews
urlpatterns = [
    path('', passengerViews.home, name="passengerHome" )
]