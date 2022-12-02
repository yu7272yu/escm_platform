# apps/blog/alarm_consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from django.http import HttpResponse

from app_manage.models.sh_user_info_sh_alarm_info import ShUserInfoShAlarmInfo
from escm_platform.common.constants import Constants


class AlarmConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.room_group_name = Constants.ALARM_INFO_GROUP + str(self.user_id)
        print('room_group_name--{}'.format(self.room_group_name))

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from room group
    async def alarm_num(self, event):
        num = event["num"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"num": num}))


# 这个是主动推送的关键,一定要写成一个函数,然后在调用
def push(id_list, message=None):
    """
    :param gropu_name: 上面定义的组的名字
    :param message: 你要返回的消息内容,可以是str,dict
    :return:
    """
    channel_layer = get_channel_layer()
    for user_id in id_list:
        user_alarm_dict = {'sh_user_info_id': user_id, 'is_read': Constants.ALARM_INFO_NOT_READ}
        user_alarm_info = ShUserInfoShAlarmInfo.objects.filter(**user_alarm_dict)
        num = Constants.DATA_NUM
        if user_alarm_info:
            num = len(user_alarm_info)

        print('group--{}'.format(Constants.ALARM_INFO_GROUP+str(user_id)))

        async_to_sync(channel_layer.group_send)(
            Constants.ALARM_INFO_GROUP+str(user_id),
            {"type": "alarm_num", "num": num},
        )
