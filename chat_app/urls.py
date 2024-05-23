from django.urls import path
from .views import index, RegisterFilterAPIView, ChatGroupList, ChatMessageList

urlpatterns = [
    path('<str:group_name>', index, name='index'),
    path('register_uuid/', RegisterFilterAPIView.as_view(), name='register'),
    path('groups/', ChatGroupList.as_view(), name='group-list'),
    path('messages/', ChatMessageList.as_view(), name='message-list'),
]
