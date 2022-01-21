from django.urls import path
from busstop import views
urlpatterns = [

    path("", views.stats, name="view-busstop-stats"),
    path("<int:busrun_id>/", views.getLocationDataForBusRun, name="get-busstopsforbusrun")
]