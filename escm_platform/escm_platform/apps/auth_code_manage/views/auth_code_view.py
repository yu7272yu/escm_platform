# coding=utf-8
from escm_platform.common.logger import Logger
from escm_platform.common.constants import Constants
from escm_platform.common.base_view import BaseView
from auth_code_manage.objects.auth_code_object import AuthCodeObject
from auth_code_manage.services.auth_code_service import AuthCodeService
from auth_code_manage.models.auth_code_model import AuthCode


class AuthCodeView(BaseView):
    """
    授权码-只有新增 更新 查询（超级管理员权限） 三个接口 不支持列表 删除
    """

    def __init__(self):
        self.auth_code_service = AuthCodeService()

    def auth_code_add(self, request):
        """
        授权码激活---录入平台--采用同一套jwt加密方式
        :param request:
        :return:
        """
        # 平台授权--需要超级管理员填写信息
        auth_company = request.POST.get('auth_company')
        auth_project = request.POST.get('auth_project')

        resource_num = int(request.POST.get('resource_num'))
        # 授权应用名称
        app_names = request.POST.get('app_names')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        if request.user.sh_user_role_name != Constants.SUPPER_ADMIN:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.NO_JURISDICTION_TO_OPERATION}

        if not all([resource_num, app_names, start_time, end_time]):
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.HAVE_NO_ENOUGH_PARAMS}

        auth_code_obj = AuthCodeObject()
        auth_code_obj.auth_company = auth_company
        auth_code_obj.auth_project = auth_project
        auth_code_obj.start_time = start_time
        auth_code_obj.end_time = end_time
        auth_code_obj.resource_num = resource_num
        auth_code_obj.app_names = app_names

        return self.auth_code_service.auth_code_add_service(auth_code_obj)

    def auth_code_update(self, request):
        """
        授权码激活---录入平台-
        :param request:
        :return:
        """
        # 平台授权--需要超级管理员填写信息
        auth_code = request.POST.get('auth_code')

        if not auth_code:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.HAVE_NO_ENOUGH_PARAMS}

        json_data = self.auth_code_service.auth_code_update_service(auth_code)

        return json_data

    def auth_code_info(self, request):
        try:
            auth_obj = AuthCode.objects.filter(data_status=Constants.DATA_IS_USED).first()

        except Exception as e:
            Logger().error('auth_code_info-error:{}'.format(e), Constants.AUTH_CODE_MANAGE_LOG)
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.WEB_REQUEST_MSG_ERROR}

        if auth_obj is None:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.HAVE_NO_EXPECT_DATA}

        data_dict = {
            'id': auth_obj.id,
            'auth_code': auth_obj.auth_code,
            'auth_company': auth_obj.auth_company,
            'auth_project': auth_obj.auth_project,
            'start_time': auth_obj.start_time,
            'end_time': auth_obj.end_time,
            'resource_num': auth_obj.resource_num,
            'app_info': [one_obj.app_name for one_obj in auth_obj.app_info.all()]
        }

        return {'code': Constants.WEB_REQUEST_CODE_OK, 'msg': Constants.WEB_REQUEST_MSG_OK, 'data': data_dict}
