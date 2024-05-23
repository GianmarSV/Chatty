import json

from django.shortcuts import render
from django.core.cache import cache
from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from uuid import uuid4

from .models import ChatGroup, ChatMessage
from .serializers import ChatMessageSerializer, ChatGroupSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse



@api_view(['GET'])
@permission_classes([AllowAny])
#@authentication_classes([JWTAuthentication])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def index(request, group_name):
    return render(request, 'chat_app/index.html',
                  {'group_name': group_name})


class RegisterFilterAPIView(APIView):
    
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    @extend_schema(
        summary="Register a websocket and generate an uuid",
        responses={200: 'Success', 400: 'Bad Request'},
    )
    def get(self, request, *args, **kwargs):
        ticket_uuid = str(uuid4())
        user = request.user
        group_name = request.query_params.get('group_name', '')
        
        # Link user to group
        chat_group, _ = ChatGroup.objects.get_or_create(name=group_name)
        user_in_group = ChatGroup.objects.filter(members__id=user.id, name=group_name)
        if not list(user_in_group):
            chat_group.members.add(user)
            chat_group.save()
        else:
            chat_group = user_in_group.first()
        
        # Cache group-message data
        data = json.dumps({
            'user_id': user.id,
            'username': user.username,
            'group_name': group_name,
            'group_id': chat_group.id})
        if request.user.is_anonymous:
            cache.set(ticket_uuid, False, settings.TICKET_EXPIRE_TIME)
        else:
            cache.set(ticket_uuid, data, settings.TICKET_EXPIRE_TIME)

        return Response({'ticket_uuid': ticket_uuid, 'username': user.username})


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


@extend_schema(
    responses={200: ChatGroupSerializer(many=True)},
    parameters=[
        OpenApiParameter(name='page', description='Page number', required=False, type=int),
        OpenApiParameter(name='page_size', description='Page size', required=False, type=int),
    ]
)
class ChatGroupList(generics.ListAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = ChatGroup.objects.all().order_by('-name')
    serializer_class = ChatGroupSerializer
    pagination_class = StandardResultsSetPagination
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


@extend_schema(
    responses={200: ChatMessageSerializer(many=True)},
    parameters=[
        OpenApiParameter(name='group_name', description='Name of the chat group', required=True, type=str),
        OpenApiParameter(name='page', description='Page number', required=False, type=int),
        OpenApiParameter(name='page_size', description='Page size', required=False, type=int),
    ]
)
class ChatMessageList(generics.ListAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ChatMessageSerializer
    pagination_class = StandardResultsSetPagination
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_queryset(self):
        group_name = self.request.query_params.get('group_name', '')
        group = get_object_or_404(ChatGroup, name=group_name)
        return ChatMessage.objects.filter(group=group).select_related('user').order_by('-send_date')
