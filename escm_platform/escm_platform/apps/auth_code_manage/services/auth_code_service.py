# coding=utf-8
import uuid
import time
from datetime import date
from datetime import timedelta
from django.db import transaction

from user_manage.models.user_info_model import UserInfo
from escm_platform.common.jwt_token import JwtToken
from escm_platform.common.constants import Constants
from escm_platform.common.logger import Logger
from escm_platform.common.obj_to_dict import ObjToDict
from auth_code_manage.models.auth_code_model import AuthCode

class AuthCodeService(object):
    def __init__(self):
        self.obj_to_dict = ObjToDict()

    def auth_code_add_service(self, add_auth_code_obj):
        """
        授权码信息不存在数据库
        :param add_auth_code_obj:
        :return:
        """
        try:
            # # 开始时间；获取今天的时间
            # start_time = date.today().strftime('%Y-%m-%d')
            # # 结束时间--
            # end_time = (date.today() + timedelta(add_auth_code_obj.use_days)).strftime('%Y-%m-%d')
            #
            # add_auth_code_obj.start_time = start_time
            # add_auth_code_obj.end_time = end_time

            auth_code_dict = self.obj_to_dict.obj_to_dict(add_auth_code_obj)

            # 生成授权码--
            add_auth_code_obj.auth_code = JwtToken().create_jwt_token(auth_code_dict)
            auth_code_dict['auth_code'] = add_auth_code_obj.auth_code

        except Exception as e:
            Logger().error('auth_code_add_service-add:{}'.format(e), Constants.AUTH_CODE_MANAGE_LOG)
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': '{}({})'.format(Constants.DATA_ADD_ERROR, e)}

        return {'code': Constants.WEB_REQUEST_CODE_OK, 'msg': Constants.DATA_ADD_OK, 'data': auth_code_dict}

    @transaction.atomic
    def auth_code_update_service(self, auth_code):
        save_id = transaction.savepoint()
        try:
            # 解析auth_code
            dict_data = JwtToken().analysis_jwt_token(auth_code)
            dict_data['auth_code'] = auth_code

            print('dict_data--{}'.format(dict_data))

            # 获取app信息
            app_names = dict_data.get('app_names')

            app_names_list = app_names.split(',')
            print('app_names_list-{}'.format(app_names_list))
            app_dict = {
                'data_status': Constants.DATA_IS_USED,
                'app_name__in': app_names_list
            }

            # 获取到app对象
            app_obj = AppInfoModel.objects.filter(**app_dict).all()
            now_app_ids = [one.id for one in app_obj]
            print('app_obj--{}'.format(app_obj))
            user_info = UserInfo.objects.exclude(user_name=Constants.SUPER_ADMIN_NAME)
            for user in user_info:
                old_app_ids = [one.id for one in user.app_info.all()]
                app_ids = list(set(now_app_ids) & set(old_app_ids))
                user.app_info.set(app_ids)


            # dict_data.delete('app_names')
            del dict_data['app_names']

            # 获取当前授权码对象
            auth_obj = AuthCode.objects.first()
            # 如果没有授权码--则直接新增
            if auth_obj is None:
                # 新生成验证码对象
                auth_obj = AuthCode.objects.create(**dict_data)
                auth_obj.app_info.add(*app_obj)

            # 更新
            else:
                auth_obj.app_info.clear()
                dict_data['update_time'] = int(time.time())
                AuthCode.objects.filter(id=auth_obj.id, update_time=auth_obj.update_time).update(
                    **dict_data)

                print('auth_obj--{}'.format(auth_obj))
                auth_obj.app_info.add(*app_obj)

            auth_code = {
                'id': auth_obj.id,
                'auth_code': auth_obj.auth_code,
                'auth_company': auth_obj.auth_company,
                'auth_project': auth_obj.auth_project,
                'start_time': auth_obj.start_time,
                'end_time': auth_obj.end_time,
                'resource_num': auth_obj.resource_num,
                'app_info': [one_obj.app_name for one_obj in app_obj]
            }
            transaction.savepoint_commit(save_id)
            return {'code': Constants.WEB_REQUEST_CODE_OK, 'msg': Constants.DATA_UPDATE_OK, 'data': auth_code}
        except Exception as e:
            transaction.savepoint_rollback(save_id)
            error_msg = '{}({})'.format(Constants.DATA_UPDATE_ERROR, e)
            Logger().error(error_msg, Constants.AUTH_CODE_MANAGE_LOG)

            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': error_msg}
