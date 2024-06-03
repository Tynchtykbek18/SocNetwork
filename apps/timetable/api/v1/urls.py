from django.urls import path

from apps.timetable.api.v1.apis import DepartmentList, StartParsingAPI, TimeTableList

app_name = "timetable"

urlpatterns = [
    path("start-parsing/", StartParsingAPI.as_view(), name="start-parsing"),
    path("departments/", DepartmentList.as_view(), name="departments"),
    path("timetables/", TimeTableList.as_view(), name="timetables"),
]
