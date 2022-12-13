# coding=utf-8
from django.db import models

from app_manage.models.base_model import BaseModel
from project_platform.common.constants import Constants


class UserInfo(BaseModel):
    user_name = models.CharField(max_length=32, verbose_name='用户账号')
    # user_name = models.BinaryField(verbose_name='用户账号')
    user_password = models.CharField(max_length=128, verbose_name='用户密码')
    email = models.CharField(max_length=32, blank=True, verbose_name='邮箱信息')
    telephone = models.CharField(max_length=16, blank=True, verbose_name='手机号码')
    nickname = models.CharField(max_length=32, blank=True, verbose_name='用户昵称')
    avatar_url = models.CharField(max_length=128, blank=True, verbose_name='头像地址')
    sh_user_role = models.ForeignKey(to='UserRole', on_delete=models.PROTECT, verbose_name='用户角色id')
    data_status = models.IntegerField(default=Constants.DATA_IS_USED, verbose_name='数据状态')

    class Meta:
        db_table = 'sh_user_info'


