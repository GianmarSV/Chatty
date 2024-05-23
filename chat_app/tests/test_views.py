import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from chat_app.models import ChatGroup, ChatMessage
from django.core.cache import cache
from random import choice, randint

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def users(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        users = [
            User.objects.get_or_create(username=f'user{i}', email=f'user{i}@example.com', password='password')
            for i in range(1, 6)
        ]
        users = [user for user, _ in users]
    return users

@pytest.fixture
def chat_groups(django_db_setup, django_db_blocker, users):
    with django_db_blocker.unblock():
        groups = [ChatGroup.objects.create(name=f'group{i}') for i in range(1, 6)]
        for group in groups:
            group.members.set(user for user in users)
    return groups

@pytest.fixture
def chat_messages(django_db_setup, django_db_blocker, chat_groups, users):
    with django_db_blocker.unblock():
        messages = []
        for group in chat_groups:
            for user in users:
                messages.append(ChatMessage.objects.create(
                    group=group, user=user, message=f'Message from {user.username} in {group.name}'
                ))
    return messages

# Test index view
def test_index_view(api_client):
    url = reverse('index', kwargs={'group_name': 'group1'})
    response = api_client.get(url)
    assert response.status_code == 200

# Test RegisterFilterAPIView
@pytest.mark.django_db
def test_register_filter_api_view(api_client, users, settings):
    url = reverse('register')
    api_client.force_authenticate(user=users[0])
    response = api_client.get(url, {'group_name': 'group2'})
    assert response.status_code == 200
    assert 'ticket_uuid' in response.data
    assert 'username' in response.data

    ticket_uuid = response.data['ticket_uuid']
    cached_data = cache.get(ticket_uuid)
    assert cached_data is not None

# Test ChatGroupList APIView
@pytest.mark.django_db
def test_chat_group_list_api_view(api_client, users):
    url = reverse('group-list')
    api_client.force_authenticate(user=users[1])
    response = api_client.get(url)
    assert response.status_code == 200
    assert 'results' in response.data

# Test ChatMessageList APIView
@pytest.mark.django_db
def test_chat_message_list_api_view(api_client, users, chat_groups, chat_messages):
    url = reverse('message-list')
    api_client.force_authenticate(user=users[2])
    response = api_client.get(url, {'group_name': chat_groups[1].name})
    assert response.status_code == 200
    assert 'results' in response.data
    assert len(response.data['results']) > 0
