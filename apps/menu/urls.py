from django.urls import path

from .views import MenuDetailAPI, parsing

app_name = "menus"

urlpatterns = [
    path("", MenuDetailAPI.as_view(), name="menu"),
    path("parsing/", parsing, name="parsing"),
]
