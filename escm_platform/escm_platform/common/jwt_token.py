# coding=utf-8
import jwt
import time
from escm_platform import settings
from django.http import JsonResponse
from escm_platform.common.constants import Constants
from escm_platform.common.time_helper import TimeHelper
from user_manage.models.user_info_model import UserInfo
from auth_code_manage.models.auth_code_model import AuthCode


class JwtToken(object):
    """
    jwt token 生成-解析 验证
    """

    def __init__(self):
        self.time_helper = TimeHelper()

    def create_jwt_token(self, payload_dict):
        """
        jwt_token 字符串生成
        :param payload_dict: token生成信息字典 {'user_name':'账号名称','create_time':‘生成时间’}
        :return: jwt_token 字符串
        """
        jwt_token = jwt.encode(payload_dict, settings.SECRET_KEY, algorithm='HS256')

        return jwt_token

    def analysis_jwt_token(self, jwt_token):
        """
        jwt_token 解析---
        :param jwt_token:
        :return: 返回信息字典
        """
        try:
            json_data = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
        except Exception as e:
            json_data = None
            print('日志记录--e--{}'.format(e))

        return json_data

    @staticmethod
    def auth_token(func):
        def auth_work1(*args):
            request = args[1]
            token = request.META.get('HTTP_AUTHORIZATION')
            request_method = str(request.path).split('/')[Constants.URL_REQUEST_METHOD_INDEX]

            # 登录请求接口不需要校验token--直接进入登录视图函数
            if request_method in [Constants.LOGIN_REQUEST_METHOD, Constants.LOGIN_CODE_METHOD,
                                  Constants.ADD_USER_ROLE_METHOD, Constants.SUPER_ADMIN_NAME_REGISTER,
                                  Constants.LOGIN_VIDEO_METHOD, Constants.MACHINE_RTSP_ACTION_METHOD,
                                  Constants.AUTH_CODE_INFO_METHOD]:
                return func(*args)

            # token为必传参数
            if token is None:
                json_data = {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.TOKEN_IS_NONE}
                return JsonResponse(json_data, safe=False)

            # 校验是否为有效token
            json_data = JwtToken().analysis_jwt_token(token)

            if json_data is None:
                json_data = {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.TOKEN_ERROR_MSG}
                return JsonResponse(json_data, safe=False)

            # 校验token是否过期
            before_date = TimeHelper().get_before_today(Constants.TOKEN_EXPIRE_DAYS)
            if int(before_date) > int(json_data.get('create_time')):
                json_data = {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.TOKEN_TIMEOUT_MSG}
                return JsonResponse(json_data, safe=False)

            # 超级管理员、更新授权码、查看授权码码请求，不需要校验授权码信息。
            user_name = json_data.get('user_name')
            if user_name != Constants.SUPER_ADMIN_NAME and request_method not in Constants.NO_CHECK_AUTH_CODE_LIST:
                # todo----------------查询授权吗权限
                # 第一 有授权码--第二且没有过期
                auth_obj = AuthCode.objects.first()

                # 表示没有授权码
                if auth_obj is None:
                    json_data = {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.AUTH_CODE_PROMPT_MSG}
                    return JsonResponse(json_data, safe=False)

                # 有授权码 且已经过期--到期时间和今天对比 todo
                if int(time.time()) >= (
                    int((time.mktime(time.strptime(auth_obj.end_time, '%Y-%m-%d')))) + 24 * 60 * 60):
                    json_data = {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.AUTH_CODE_PROMPT_MSG}
                    return JsonResponse(json_data, safe=False)

            # 获取user信息
            try:
                user_info_obj = UserInfo.objects.filter(user_name=user_name, data_status=Constants.DATA_IS_USED) \
                    .values('sh_user_role__role_name', 'sh_user_role_id', 'id').first()

                if user_info_obj is None:
                    json_data = {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.SELECT_SQL_ERROR}
                    return JsonResponse(json_data, safe=False)

            except Exception as e:
                print(e)
                json_data = {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.SELECT_SQL_ERROR}
                return JsonResponse(json_data, safe=False)

            # 重新user 属性
            request.user.user_name = user_name
            request.user.sh_user_role_name = user_info_obj.get('sh_user_role__role_name')
            request.user.sh_user_role_id = user_info_obj.get('sh_user_role_id')
            request.user.sh_user_info_id = user_info_obj.get('id')

            return func(*args)

        return auth_work1
