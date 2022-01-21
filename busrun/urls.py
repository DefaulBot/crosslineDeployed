from django.urls import path
from busrun import views


urlpatterns = [
    path("manage/", views.manage, name="manage-busrun"),
    path("manage/<int:busrun_id>",views.addLocation, name="add_busrun_locations"),
    path("location/create/", views.createLocation, name="create-location"),
]