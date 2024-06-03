from django.urls import path

from apps.story.api.v1.apis.story_api import (
    StoryCreate,
    StoryDetail,
    StoryList,
    UserStoryList,
)

app_name = "story"


urlpatterns = [
    path("create/", StoryCreate.as_view()),
    path("list/", StoryList.as_view()),
    path("user-stories/", UserStoryList.as_view()),
    path("detail/<int:pk>/", StoryDetail.as_view()),
]
