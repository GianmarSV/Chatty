# Chatty App

This project helps people to comunicate in groups! A person can create an account and securely use the web app to send message to infinite groups.

### How to set up the project

1. All the resources are created with a docker compose definition
```sh
docker-compose up --build --force-recreate --no-deps
```
2. Inside of django_app container run the commands below to initialize the data
```sh
python manage.py migrate
python manage.py populate_chat_data
```
We are ready!

### API Documentation

I'm using `drf-spectacular` to document the API, it's becouse this library uses OpenAPI 3.

SCHEMA SWAGGER UI -> http://localhost/api/schema/swagger-ui/
SCHEMA REDOC -> http://localhost/api/schema/redoc/

### Use the web app

1. Create an account http://127.0.0.1/signin/ (create an account option)
2. Login http://127.0.0.1/signin/
3. After the login type the group name! It'll redirect to the group, example: http://127.0.0.1/chat/group1
4. CHange manually the group, change the url. Example http://127.0.0.1/chat/new_group

### Limitations

If someone tries to make spam (more than 1 message by second), the backend will sned a message `Too many messages, please slow down!` limitating the messages at 1 per second at most.

```python
        'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',  # Anonymous user max 100 request per day 
        'user': '1000/hour',  # Authenticated user, 1000 request by hour
        'message': '1/second',  # Websockets messages, 1 message by second
```

### Test coverage
All the views were tested with `pytest-django` with coverage of 98%

```sh
Name                                               Stmts   Miss  Cover
----------------------------------------------------------------------
auth_app/__init__.py                                   0      0   100%
auth_app/admin.py                                      1      0   100%
auth_app/apps.py                                       4      0   100%
auth_app/migrations/0001_initial.py                    7      0   100%
auth_app/migrations/__init__.py                        0      0   100%
auth_app/models.py                                    15      1    93%
auth_app/serializers.py                               25      1    96%
auth_app/tests/__init__.py                             0      0   100%
auth_app/tests/test_views.py                          44      0   100%
auth_app/urls.py                                       4      0   100%
auth_app/views.py                                     29      1    97%
chat/__init__.py                                       0      0   100%
chat/settings.py                                      31      0   100%
chat/spectacular_throttling.py                        12      0   100%
chat/throttling.py                                     5      1    80%
chat/urls.py                                           4      0   100%
chat_app/__init__.py                                   0      0   100%
chat_app/admin.py                                      1      0   100%
chat_app/apps.py                                       4      0   100%
chat_app/migrations/0001_initial.py                    7      0   100%
chat_app/migrations/0002_alter_chatgroup_name.py       4      0   100%
chat_app/migrations/__init__.py                        0      0   100%
chat_app/models.py                                    15      2    87%
chat_app/serializers.py                               11      0   100%
chat_app/tests/__init__.py                             0      0   100%
chat_app/tests/test_views.py                          62      0   100%
chat_app/urls.py                                       3      0   100%
chat_app/views.py                                     66      2    97%
----------------------------------------------------------------------
TOTAL                                                354      8    98%
```