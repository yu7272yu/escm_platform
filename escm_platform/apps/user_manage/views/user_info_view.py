# coding=utf-8
from escm_platform.common.base_view import BaseView
from user_manage.objects.user_info_object import UserObject
from user_manage.services.user_info_service import UserInfoService
from escm_platform.common.constants import Constants
from django.http import QueryDict
from escm_platform.common.logger import Logger
from user_manage.models.user_role_model import UserRoleModel


class UserInfoView(BaseView):
    """
    用户信息视图类--增删改查
    """

    def __init__(self):
        self.user_info_service = UserInfoService()

    def user_info_list(self, request):
        """
        用户列表信息视图函数
        :param request:
        :return:
        """
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))

        sh_user_role_id = request.GET.get('sh_user_role_id')
        create_start_time = request.GET.get('create_start_time')
        create_end_time = request.GET.get('create_end_time')

        # 不清楚后期查询字段以及数据表名称，以对象的形式传递数据。
        query_user_obj = UserObject()
        query_user_obj.page = page
        query_user_obj.limit = limit
        query_user_obj.sh_user_role_id = sh_user_role_id
        query_user_obj.create_start_time = create_start_time
        query_user_obj.create_end_time = create_end_time

        json_data = self.user_info_service.user_info_list_service(query_user_obj, request)

        return json_data

    # 获取个人信息--个人中心
    def user_info(self, request):
        # 个人中心
        sh_user_info_id = request.GET.get('sh_user_info_id')

        if not sh_user_info_id:
            sh_user_info_id = request.user.sh_user_info_id

        json_data = self.user_info_service.user_info_service(sh_user_info_id)

        return json_data

    def get_role_app_info(self, request):
        """
        用户角色&用户应用中心权限列表--谨防时时刷新
        :param request:
        :return:
        """
        sh_user_info_id = request.user.sh_user_info_id

        heart_beat_flag = True

        json_data = self.user_info_service.user_info_service(sh_user_info_id, heart_beat_flag)

        return json_data

    def user_info_register(self, request):
        # 超级管理员注册接口-不对外开发
        user_name = request.POST.get('user_name')
        user_password = request.POST.get('user_password')

        if not all([user_name, user_password]):
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.HAVE_NO_ENOUGH_PARAMS}

        if user_name != Constants.SUPER_ADMIN_NAME:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.SUPER_ADMIN_NAME_IS_ERROR}

        # 获取超级管理员id
        super_admin_dict = {
            'data_status': Constants.DATA_IS_USED,
            'role_name': Constants.SUPPER_ADMIN
        }
        # 查询超级管理员的id
        try:
            super_admin_obj = UserRoleModel.objects.filter(**super_admin_dict).first()

        except Exception as e:
            Logger().error('user_info_register：{}'.format(e), Constants.USER_MANAGE_LOG)
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.SELECT_SQL_ERROR}

        if not super_admin_obj:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.ADD_SUPER_ADMIN_ROLE}

        # 生成数据对象
        add_user_obj = UserObject()
        add_user_obj.user_name = user_name
        add_user_obj.user_password = user_password
        add_user_obj.sh_user_role_id = super_admin_obj.id

        json_data = self.user_info_service.user_info_add_service(add_user_obj)

        return json_data

    def user_info_add(self, request):
        """
        用户信息新增视图函数
        :param request:
        :return:
        """
        user_name = request.POST.get('user_name')
        user_password = request.POST.get('user_password')
        sh_user_role_id = request.POST.get('sh_user_role_id')

        # 头像信息---file数据流
        avatar_picture = request.FILES.get('avatar_picture')

        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        nickname = request.POST.get('nickname')

        if not all([user_name, user_password, sh_user_role_id]):
            return {'code': Constants.WEB_REQUEST_CODE_OK, 'msg': Constants.HAVE_NO_ENOUGH_PARAMS}

        # 生成数据对象
        add_user_obj = UserObject()
        add_user_obj.user_name = user_name
        add_user_obj.user_password = user_password
        add_user_obj.sh_user_role_id = sh_user_role_id
        add_user_obj.avatar_picture = avatar_picture
        add_user_obj.email = email
        add_user_obj.telephone = telephone
        add_user_obj.nickname = nickname

        json_data = self.user_info_service.user_info_add_service(add_user_obj)

        return json_data

    def user_info_delete(self, request):
        """
        用户信息删除视图函数---支持批量传参
        :param request:
        :return:
        """
        # 支持批量删除---传递的是数组（1,2,3,4）
        data = QueryDict(request.body)
        sh_user_info_ids = data.get('sh_user_info_ids')

        # sh_user_info_ids = request.POST.get('sh_user_info_ids')
        print('sh_user_info_ids--{}--{}'.format(sh_user_info_ids, type(sh_user_info_ids)))

        if not sh_user_info_ids:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.HAVE_NO_ENOUGH_PARAMS}

        user_role_name = request.user.sh_user_role_name

        if user_role_name not in [Constants.SUPPER_ADMIN, Constants.ADMIN]:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.NO_JURISDICTION_TO_OPERATION}

        delete_user_obj = UserObject()
        delete_user_obj.sh_user_info_id = sh_user_info_ids

        return self.user_info_service.user_info_delete_service(delete_user_obj)

    def user_info_update(self, request):
        """
        用户信息更新视图函数--密码要单独更新--主要更新为 昵称 电话 邮箱 头像--以及角色
        :param request:
        :return:
        """
        # 删除用户信息---更新数据状态
        sh_user_info_id = request.POST.get('sh_user_info_id')

        # 默认是有当前字段
        avatar_picture = request.FILES.get('avatar_picture')
        print('avatar_picture--{}'.format(avatar_picture))

        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        nickname = request.POST.get('nickname')
        sh_user_role_id = request.POST.get('sh_user_role_id')

        if not all([sh_user_info_id, sh_user_role_id]):
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.HAVE_NO_ENOUGH_PARAMS}

        update_user_obj = UserObject()
        update_user_obj.sh_user_info_id = sh_user_info_id
        update_user_obj.email = email
        update_user_obj.telephone = telephone
        update_user_obj.nickname = nickname
        update_user_obj.avatar_picture = avatar_picture
        update_user_obj.sh_user_role_id = sh_user_role_id

        json_data = self.user_info_service.user_info_update_service(update_user_obj)

        return json_data

    # 用户更新密码--
    def user_info_update_password(self, request):
        sh_user_info_id = request.POST.get('sh_user_info_id')
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password1')

        if not all([sh_user_info_id, old_password, new_password1, new_password2]):
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.HAVE_NO_ENOUGH_PARAMS}

        if new_password1 != new_password2:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.TWO_TIME_TWO_PASSWORD}

        update_user_obj = UserObject()
        update_user_obj.sh_user_info_id = sh_user_info_id
        update_user_obj.old_password = old_password
        update_user_obj.new_password1 = new_password1
        update_user_obj.new_password2 = new_password2

        json_data = self.user_info_service.user_info_update_password_service(update_user_obj)

        return json_data

    def user_info_reset_password(self, request):
        sh_user_info_id = request.POST.get('sh_user_info_id')

        if not sh_user_info_id:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.HAVE_NO_ENOUGH_PARAMS}

        # 重置
        json_data = self.user_info_service.user_info_reset_password_service(sh_user_info_id, request)

        return json_data

    def user_app_authorization(self, request):
        sh_app_info_ids = request.POST.get('sh_app_info_ids')
        sh_user_info_id = request.POST.get('sh_user_info_id')

        if not sh_user_info_id:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.HAVE_NO_ENOUGH_PARAMS}

        if sh_app_info_ids:
            sh_app_info_ids = [int(i) for i in str(sh_app_info_ids).split(',')]
        else:
            sh_app_info_ids = []

        auth_user_obj = UserObject()
        auth_user_obj.sh_user_info_id = sh_user_info_id
        auth_user_obj.sh_app_info_ids = sh_app_info_ids

        json_data = self.user_info_service.user_app_authorization_service(auth_user_obj)

        return json_data
