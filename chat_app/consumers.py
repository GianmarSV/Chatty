
import json
from urllib.parse import parse_qsl
from asgiref.sync import sync_to_async
from django.core.cache import cache
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        self.room_group_name = f"chat_{self.group_name}"

        query_string = self.scope['query_string'].decode('utf-8')
        query_params = dict(parse_qsl(query_string))
        ticket_uuid = query_params.get('ticket_uuid')
        self.scope['has_ticket'] = cache.get(ticket_uuid)

        # XXX: Destroy the ticket for performance and security purposes
        data = json.loads(cache.get(ticket_uuid))
        username = data['username']
        #group_name = data['group_name']
        if not username:
            raise Exception('ticket not found')
        
        # Set up the throttling
        from chat.throttling import MessageRateThrottle
        self.user_id = data['user_id']
        self.throttle = MessageRateThrottle()

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        await self.send(text_data=json.dumps({
            'message': 'Connection established',
            'username': 'Chatty system'
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        if not self.throttle.allow_request(None, self):
            await self.send(text_data=json.dumps({
                'message': 'Too many messages, please slow down!',
                'username': 'Chatty system'
            }))
            #await self.close()
            return

        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        ticket_uuid = text_data_json['uuid']
        data = json.loads(cache.get(ticket_uuid))
        username = data['username']
        user_id = data['user_id']
        group_id = data['group_id']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

        # Save chat message
        from .models import ChatMessage

        await sync_to_async(ChatMessage.objects.create)(
            user_id=user_id,
            group_id=group_id,
            message=message
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))
