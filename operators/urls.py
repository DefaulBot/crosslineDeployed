from django.urls import path
from operators import views

urlpatterns = [
    path("", views.manage , name="operator-manage"),
    path("scan/", views.scan, name="scanqr"),
    path("view-tickets/", views.viewTickets, name="view-passenger-tickets"),
    path("<int:operator_id>/delete", views.delete, name="operator-delete")
]