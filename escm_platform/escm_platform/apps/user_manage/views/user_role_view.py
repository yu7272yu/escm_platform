# coding=utf-8
from django.http import QueryDict
from escm_platform.common.base_view import BaseView
from escm_platform.common.constants import Constants
from user_manage.models.user_role_model import UserRole
from user_manage.services.user_role_service import UserRoleService
from escm_platform.common.logger import Logger
# from escm_platform.common.scheduler_center import scheduler


class UserRoleView(BaseView):
    """
    用户角色管理入口
    """

    def __init__(self):
        self.user_role_service = UserRoleService()

    # 获取用户角色信息--当前接口对外开放--在用户管理界面--不同角色拿到的类型不一致 todo--需要优化
    def user_role_list(self, request):
        # 获取当前用户的角色id 以及角色
        user_role_name = request.user.sh_user_role_name
        user_role_id = request.user.sh_user_role_id

        try:
            exclude_dict = {}
            filter_dict = {'data_status': Constants.DATA_IS_USED}

            if user_role_name == Constants.SUPPER_ADMIN:
                exclude_dict['id__in'] = [user_role_id]

            elif user_role_name == Constants.ADMIN:
                super_admin_dict = {
                    'data_status': Constants.DATA_IS_USED,
                    'role_name': Constants.SUPPER_ADMIN
                }
                # 查询超级管理员的id
                super_admin_obj = UserRole.objects.filter(**super_admin_dict).first()

                if super_admin_obj is None:
                    return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.SELECT_SQL_ERROR}

                exclude_dict['id__in'] = [user_role_id, super_admin_obj.id]

            # 其余角色不具备请求
            else:
                return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.HAVE_NO_EXPECT_DATA}

            roles_obj = UserRole.objects.exclude(**exclude_dict).filter(**filter_dict).all()

        except Exception as e:
            Logger().error('user_role_list：{}'.format(e), Constants.USER_MANAGE_LOG)

            # 程序异常 需要修复bug--返回给用户的信息为无符号条件？
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.SELECT_SQL_ERROR}

        if roles_obj is None:
            roles_obj = []

        role_list = [{'name': one_obj.role_name, 'id': one_obj.id} for one_obj in roles_obj]

        return {'code': Constants.WEB_REQUEST_CODE_OK, 'msg': Constants.WEB_REQUEST_MSG_OK, 'data': role_list}

    # 程序内部调用API
    def user_role_add(self, request):
        role_name = request.POST.get('role_name')

        if not role_name:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.HAVE_NO_ENOUGH_PARAMS}

        json_data = self.user_role_service.user_role_add_service(role_name)

        return json_data

    # 程序内部调用API
    def user_role_delete(self, request):
        # 删除用户信息---更新数据状态
        data = QueryDict(request.body)
        user_role_id = data.get('sh_user_role_id')

        user_role_name = request.user.sh_user_role_name

        if user_role_name != Constants.SUPPER_ADMIN:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.NO_JURISDICTION_TO_OPERATION}

        if not user_role_id:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.HAVE_NO_ENOUGH_PARAMS}

        json_data = self.user_role_service.user_role_delete_service(user_role_id)

        return json_data

    # 只能删除--不能编辑
    def user_role_update(self, request):
        pass
