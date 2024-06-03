from django.urls import path

from apps.complaint.api.v1.apis.complaint_apis import (
    ComplaintCreateAPIView,
    PostsWithComplaintsListView,
)

app_name = "reported"


urlpatterns = [
    path("create/", ComplaintCreateAPIView.as_view()),
    path("list/", PostsWithComplaintsListView.as_view()),
]
