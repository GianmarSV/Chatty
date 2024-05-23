from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.models import Q
from chat_app.models import ChatGroup, ChatMessage
from random import choice, randint
from faker import Faker


fake = Faker()
User = get_user_model()

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        # Create superuser
        username = 'admin'
        email = 'admin@test.com'
        password = 'admin'
        user = User.objects.create_superuser(username=username, email=email, password=password)

        # Create sample users if not exist
        for i in range(1,11):
            username = f'username{i}'
            email = f'{username}@test.com'
            User.objects.create_user(username=username, email=email, password='pass')

        users = User.objects.filter(~Q(username='admin'))

        # Create sample chat groups
        for i in range(1,6):
            group_name = f'group{i}'
            group = ChatGroup.objects.create(name=group_name)
            group.members.set(choice(users) for _ in range(randint(1, 5)))

        groups = ChatGroup.objects.all()

        # Create sample chat messages
        for group in groups:
            for _ in range(randint(20, 50)):
                user = choice(group.members.all())
                ChatMessage.objects.create(
                    user=user,
                    group=group,
                    message=fake.text(max_nb_chars=200)
                )
