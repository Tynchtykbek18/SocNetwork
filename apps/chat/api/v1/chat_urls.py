from django.urls import path

from apps.chat.api.v1.apis.chat_apis import StartConvoView, GetConversationView, ConversationsView, \
    DeleteConversationView, DeleteMessageView

app_name = "chats"

urlpatterns = [
    path("start/", StartConvoView.as_view(), name="start_convo"),
    path("<int:convo_id>/", GetConversationView.as_view(), name="get_conversation"),
    path("", ConversationsView.as_view(), name="conversations"),
    path("delete/conversation/<int:id>/", DeleteConversationView.as_view(), name="delete_convo"),
    path("delete/message/<int:id>/", DeleteMessageView.as_view(), name="delete_message"),
]
