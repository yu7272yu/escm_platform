# coding=utf-8
# from app_manage.models.sh_user_info_sh_alarm_info import ShUserInfoShAlarmInfo
from project_platform.settings import SECRET_KEY
from project_platform.common.constants import Constants
from project_platform.common.sha256_encryption import ShaEncryption
from project_platform.common.jwt_token import JwtToken
from project_platform.common.time_helper import TimeHelper
from user_manage.models.user_info_model import UserInfo
from project_platform.common.logger import Logger


class UserLoginService(object):
    def __init__(self):
        self.sha_encryption = ShaEncryption()
        self.jwt_token = JwtToken()
        self.time_helper = TimeHelper()

    def user_login_service(self, user_info_obj):
        # 校验密码--获取当前用户的对象信息
        print(user_info_obj.user_name)
        query_dict = {
            'user_name__contains': user_info_obj.user_name,
            'user_name': user_info_obj.user_name,
            'data_status': Constants.DATA_IS_USED
        }

        try:
            user_obj = UserInfo.objects.filter(**query_dict).first()
        except Exception as e:
            Logger().error('user_login_service-get:{}'.format(e), Constants.USER_MANAGE_LOG)
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.SELECT_SQL_ERROR}

        # 用户名错误--
        if user_obj is None:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.PASSWORD_ERROR_MSG}

        # 密码校验
        user_password = user_obj.user_password
        # 加密用户传递密码作对比
        origin_password = self.sha_encryption.add_sha256(user_info_obj.user_password, SECRET_KEY)

        if user_password != origin_password:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.PASSWORD_ERROR_MSG}

        # token 生成基础数据---
        user_info_dict = {
            'user_name': user_obj.user_name,
            'create_time': self.time_helper.get_today()
        }
        app_list = [one.app_name for one in user_obj.app_info.filter(data_status=Constants.DATA_IS_USED).all()]

        user_alarm_dict = {'sh_user_info_id': user_obj.id, 'is_read': Constants.ALARM_INFO_NOT_READ}
        # user_alarm_info = ShUserInfoShAlarmInfo.objects.filter(**user_alarm_dict)
        num = Constants.DATA_NUM
        # if user_alarm_info:
        #     num = len(user_alarm_info)

        user_info_dict = {
            'token': self.jwt_token.create_jwt_token(user_info_dict),
            'id': user_obj.id,
            'sh_user_info_id': user_obj.id,
            'user_name': user_obj.user_name,
            'sh_user_role_id': user_obj.sh_user_role.id,
            'role_name': user_obj.sh_user_role.role_name,
            'nickname': user_obj.nickname,
            'telephone': user_obj.telephone,
            'email': user_obj.email,
            'avatar_url': user_obj.avatar_url,
            'create_time': self.time_helper.time_int_to_date(user_obj.create_time),
            'update_time': self.time_helper.time_int_to_date(user_obj.update_time),
            'app_list': app_list,
            'num': num
        }

        return {'code': Constants.WEB_REQUEST_CODE_OK, 'msg': Constants.LOGIN_SUCCESS, 'data': user_info_dict}
