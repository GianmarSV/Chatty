FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . /app/

#CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "chat.asgi:application"]
RUN python manage.py collectstatic --noinput
