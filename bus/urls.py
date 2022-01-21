from django.urls import path
from bus import views

urlpatterns = [
    path("", views.manage, name="manage-bus")
]