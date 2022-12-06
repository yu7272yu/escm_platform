# coding=utf-8
from django.db import models

from app_manage.models.base_model import BaseModel
from escm_platform.common.constants import Constants


class AuthCode(BaseModel):
    auth_code = models.TextField(blank=True, verbose_name='授权码信息')
    auth_company = models.CharField(max_length=64, blank=True, verbose_name='授权方公司')
    auth_project = models.CharField(max_length=64, blank=True, verbose_name='授权项目名称')
    # use_days = models.IntegerField(verbose_name='授权时长-单位天')
    resource_num = models.IntegerField(blank=True, verbose_name='授权接入设备数量')
    # 规避int类型不能为空
    start_time = models.CharField(max_length=16, blank=True, verbose_name='激活时间')
    end_time = models.CharField(max_length=16, blank=True, verbose_name='结束时间')
    data_status = models.IntegerField(default=Constants.DATA_IS_USED, verbose_name='数据状态')

    class Meta:
        db_table = 'sh_authorization_code'