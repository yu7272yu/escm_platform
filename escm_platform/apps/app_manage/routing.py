from django.urls import re_path

from app_manage.consumers.alarm_consumers import AlarmConsumer

websocket_urlpatterns = [
    # re_path(r'ws/alarm/(?P<user_id>\w+)/$', AlarmConsumer.as_asgi()),
]