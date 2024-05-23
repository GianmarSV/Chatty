from rest_framework import serializers
from .models import ChatGroup, ChatMessage


class ChatGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatGroup
        fields = ['id', 'name', 'members']

class ChatMessageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'user', 'group', 'message', 'send_date', 'username']
