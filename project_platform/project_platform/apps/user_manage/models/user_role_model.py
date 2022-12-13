# coding=utf-8
from django.db import models

from app_manage.models.base_model import BaseModel
from project_platform.common.constants import Constants


class UserRole(BaseModel):
    role_name = models.CharField(max_length=32, verbose_name='角色名称')
    description = models.TextField(blank=True, verbose_name='角色名称')
    data_status = models.IntegerField(default=Constants.DATA_IS_USED, verbose_name='数据状态')

    class Meta:
        db_table = 'sh_user_role'
