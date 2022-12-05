# coding=utf-8
import time
from escm_platform.common.constants import Constants
from user_manage.models.user_role_model import UserRole
from escm_platform.common.logger import Logger


class UserRoleService(object):
    def __init__(self):
        pass

    def user_role_add_service(self, role_name):
        # 查询当前数据是否已存在。
        try:
            user_role_obj = UserRole.objects.filter(data_status=Constants.DATA_IS_USED,
                                                         role_name=role_name).first()

        except Exception as e:
            Logger().error('user_role_add_service-get:{}'.format(e), Constants.USER_MANAGE_LOG)

            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.SELECT_SQL_ERROR}

        if user_role_obj:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.DATA_ALREADY_EXISTS}

        # 不存在，则新增
        try:
            add_role_obj = UserRole.objects.create(role_name=role_name)
        except Exception as e:
            Logger().error('user_role_add_service-add:{}'.format(e), Constants.USER_MANAGE_LOG)
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.DATA_ADD_ERROR}

        role_dict = {
            'id': add_role_obj.id,
            'sh_user_role_id': add_role_obj.id,
            'role_name': add_role_obj.role_name
        }

        return {'code': Constants.WEB_REQUEST_CODE_OK, 'msg': Constants.DATA_ADD_OK, 'data': role_dict}

    def user_role_delete_service(self, user_role_id):
        # 查询当前数据对象是否存在
        try:
            user_role_obj = UserRole.objects.filter(id=user_role_id).first()

        except Exception as e:
            Logger().error('user_role_delete_service-get:{}'.format(e), Constants.USER_MANAGE_LOG)

            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.SELECT_SQL_ERROR}

        if user_role_obj is None:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.OBJ_DELETE_IS_NOT_EXISTS}

        try:
            res = UserRole.objects.filter(id=user_role_id, update_time=user_role_obj.update_time).update(
                data_status=Constants.DATA_IS_DELETED, update_time=int(time.time()))

        except Exception as e:
            Logger().error('user_role_delete_service-update:{}'.format(e), Constants.USER_MANAGE_LOG)
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.DATA_DELETE_ERROR}

        if not res:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.DATA_IS_CHANGED}

        return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.DATA_DELETE_OK}
