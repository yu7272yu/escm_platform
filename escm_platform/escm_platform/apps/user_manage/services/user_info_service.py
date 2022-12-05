# coding=utf-8
import os
import time

from config import Config
from escm_platform.common.fdfs_util.fdfs_util import FastDfsUtil
from escm_platform.settings import SECRET_KEY
from user_manage.models.user_info_model import UserInfo
from user_manage.models.user_role_model import UserRole
from escm_platform.common.constants import Constants
from escm_platform.common.obj_to_dict import ObjToDict
from escm_platform.common.sha256_encryption import ShaEncryption
from escm_platform.common.time_helper import TimeHelper
from django.db import transaction
from escm_platform.common.logger import Logger
# from app_manage.models.app_info_model import AppInfoModel


class UserInfoService(object):
    def __init__(self):
        self.sha_encryption = ShaEncryption()
        self.time_helper = TimeHelper()

    def user_info_list_service(self, query_user_obj, request):
        kwargs = {'data_status': Constants.DATA_IS_USED}

        if query_user_obj.sh_user_role_id:
            kwargs['sh_user_role_id'] = query_user_obj.sh_user_role_id

        if query_user_obj.create_start_time:
            kwargs['create_time__gte'] = query_user_obj.create_start_time

        if query_user_obj.create_end_time:
            kwargs['create_time__lt'] = query_user_obj.create_end_time

        try:
            # 根据用户角色--展示不同的信息--root 超级管理员展示--
            if request.user.sh_user_role_name == Constants.SUPPER_ADMIN:
                users_obj = UserInfo.objects.exclude(sh_user_role_id=request.user.sh_user_role_id) \
                    .filter(**kwargs).order_by('-id')

            # 普通管理员--则列表中只显示普通用户的
            else:
                # 获取普通用户的角色对应的id
                q_role_dict = {'role_name': Constants.USER, 'data_status': Constants.DATA_IS_USED}
                uer_role_obj = UserRole.objects.filter(**q_role_dict).values('id').first()

                # 筛选添加只有普通用户id
                kwargs['sh_user_role_id'] = uer_role_obj.get('id')
                users_obj = UserInfo.objects.filter(**kwargs).order_by('-id')

        except Exception as e:
            users_obj = None
            Logger().error('user_info_list_service:{}'.format(e), Constants.USER_MANAGE_LOG)

        if not users_obj:
            return {'code': Constants.WEB_REQUEST_CODE_OK, 'msg': Constants.HAVE_NO_EXPECT_DATA,
                    'data': Constants.DATA_DETAIL, 'num': Constants.DATA_NUM}

        # 获取查询数据总数
        list_num = users_obj.count()

        start_index = (query_user_obj.page - 1) * query_user_obj.limit
        end_index = query_user_obj.page * query_user_obj.limit
        return_list = []
        for one_obj in users_obj[start_index: end_index]:
            one_dict = {
                'id': one_obj.id,
                'sh_user_info_id': one_obj.id,
                'user_name': one_obj.user_name,
                'sh_user_role_id': one_obj.sh_user_role.id,
                'role_name': one_obj.sh_user_role.role_name,
                'nickname': one_obj.nickname,
                'telephone': one_obj.telephone,
                'email': one_obj.email,
                'avatar_url': one_obj.avatar_url,
                'create_time': self.time_helper.time_int_to_date(one_obj.create_time),
                'update_time': self.time_helper.time_int_to_date(one_obj.update_time)
            }

            app_list = [one.app_name for one in one_obj.app_info.filter(data_status=Constants.DATA_IS_USED).all()]
            one_dict['app_list'] = app_list

            return_list.append(one_dict)

        return {'code': Constants.WEB_REQUEST_CODE_OK, 'msg': Constants.WEB_REQUEST_MSG_OK, 'num': list_num,
                'data': return_list}

    def user_info_service(self, sh_user_info_id, heart_beat_flag=None):
        try:
            user_obj = UserInfo.objects.filter(id=sh_user_info_id).first()

        except Exception as e:
            Logger().error('user_info_service:{}'.format(e), Constants.USER_MANAGE_LOG)
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.SELECT_SQL_ERROR}

        if user_obj is None:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.OBJ_DELETE_IS_NOT_EXISTS}

        app_name_list = [one.app_name for one in user_obj.app_info.filter(data_status=Constants.DATA_IS_USED).all()]
        app_id_list = [one.id for one in user_obj.app_info.filter(data_status=Constants.DATA_IS_USED).all()]

        if heart_beat_flag:
            user_info_dict = {
                'id': user_obj.id,
                'sh_user_info_id': user_obj.id,
                'sh_user_role_id': user_obj.sh_user_role.id,
                'role_name': user_obj.sh_user_role.role_name,
                'app_name_list': app_name_list,
                'app_id_list': app_id_list
            }
        else:
            user_info_dict = {
                'id': user_obj.id,
                'sh_user_info_id': user_obj.id,
                'user_name': user_obj.user_name,
                'sh_user_role_id': user_obj.sh_user_role.id,
                'role_name': user_obj.sh_user_role.role_name,
                'nickname': user_obj.nickname,
                'telephone': user_obj.telephone,
                'email': user_obj.email,
                'avatar_url': user_obj.avatar_url,
                'create_time': user_obj.create_time,
                'update_time': user_obj.update_time,
                'app_name_list': app_name_list
            }

        return {'code': Constants.WEB_REQUEST_CODE_OK, 'msg': Constants.WEB_REQUEST_MSG_OK, 'data': user_info_dict}

    def user_info_add_service(self, user_obj):
        # 查询当前数据库是否已有重名账号
        user_dict = {'user_name': user_obj.user_name,
                     'user_name__contains': user_obj.user_name,
                     'data_status': Constants.DATA_IS_USED}
        q_user_obj = UserInfo.objects.filter(**user_dict).first()

        if q_user_obj:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.USER_NAME_IS_EXISTS}

        # 将头像上传fdfs 存储url todo--------
        data = {}
        if user_obj.avatar_picture:
            # todo --调用上传文件--生成url地址
            # 将图片上传至fdfs，并获取url地址
            file_ext_name = os.path.splitext(user_obj.avatar_picture.name)[1]
            res = FastDfsUtil().upload_by_buffer(user_obj.avatar_picture.read(), file_ext_name)
            if res['code'] == Constants.WEB_REQUEST_CODE_ERROR:
                return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.PIC_UPLOAD_ERROR}
            data = res['data']
            picture_url = Config.fdfs_nginx_ip + data['Remote file_id'].decode('utf-8')
            user_obj.avatar_url = picture_url
            user_obj.avatar_picture = None

        # 加密密码
        user_obj.user_password = self.sha_encryption.add_sha256(user_obj.user_password, SECRET_KEY)

        # 生成字典对象
        add_dict = ObjToDict().obj_to_dict(user_obj)

        try:
            add_user_obj = UserInfo.objects.create(**add_dict)
        except Exception as e:
            Logger().error('user_info_add_service:{}'.format(e), Constants.USER_MANAGE_LOG)
            if data:
                FastDfsUtil().delete(data['Remote file_id'])
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.DATA_ADD_ERROR}

        return {'code': Constants.WEB_REQUEST_CODE_OK, 'msg': Constants.DATA_ADD_OK, 'sh_user_info_id': add_user_obj.id}

    @transaction.atomic
    def user_info_delete_service(self, delete_user_obj):
        """
        前面已经有权限控制--
        :param delete_user_obj:
        :param request:
        :return:
        """
        save_id = transaction.savepoint()
        try:
            for sh_user_info_id in delete_user_obj.sh_user_info_id.split(','):
                # 保证并发异常--遍历操作
                user_obj = UserInfo.objects.filter(id=sh_user_info_id).first()

                if user_obj is None:
                    delete_user_obj.option_flag = True
                    error_msg = '{}(id:{}-{})'.format(Constants.DATA_DELETE_ERROR, sh_user_info_id,
                                                      Constants.OBJ_DELETE_IS_NOT_EXISTS)
                    delete_user_obj.error_msg = error_msg
                    Logger().error(error_msg, Constants.USER_MANAGE_LOG)
                    break

                res = UserInfo.objects.filter(id=sh_user_info_id, update_time=user_obj.update_time).update(
                    data_status=Constants.DATA_IS_DELETED, update_time=int(time.time()))

                # 批量操作有一个失败则全部失败
                if not res:
                    delete_user_obj.option_flag = True
                    error_msg = '{}(id:{}-{})'.format(Constants.DATA_DELETE_ERROR, sh_user_info_id,
                                                      Constants.DATA_IS_CHANGED)
                    delete_user_obj.error_msg = error_msg
                    Logger().error(error_msg, Constants.USER_MANAGE_LOG)
                    break

            # 有删除出现异常状态--则直接回滚 且返回提示
            if delete_user_obj.option_flag:
                transaction.savepoint_rollback(save_id)
                return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': delete_user_obj.error_msg}

            # 没有异常 则提交事务
            transaction.savepoint_commit(save_id)
            return {'code': Constants.WEB_REQUEST_CODE_OK, 'msg': Constants.DATA_DELETE_OK}

        # 其余异常--回滚
        except Exception as e:
            transaction.savepoint_rollback(save_id)
            error_msg = '{}-{}'.format(Constants.DATA_DELETE_ERROR, e)
            Logger().error(error_msg, Constants.USER_MANAGE_LOG)

            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': error_msg}

    def user_info_update_service(self, update_user_obj):
        # 获取当前数据对象
        try:
            user_obj = UserInfo.objects.filter(id=update_user_obj.sh_user_info_id).first()

        except Exception as e:
            Logger().error('user_info_update_service-get:{}'.format(e), Constants.USER_MANAGE_LOG)
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.SELECT_SQL_ERROR}

        if user_obj is None:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.OBJ_DELETE_IS_NOT_EXISTS}

        # 对头像做处理
        data = {}
        origin_data = {}
        if update_user_obj.avatar_picture:
            # todo --调用上传文件--生成url地址
            # 获取原图片地址
            # origin_data['Remote file_id'] = user_obj.avatar_url.split(Constants.FDFS_NGINX_IP)[1] if len(user_obj.avatar_url.split(Constants.FDFS_NGINX_IP)) >= 1 else ''
            # 将图片上传至fdfs，并获取url地址
            file_ext_name = os.path.splitext(update_user_obj.avatar_picture.name)[1]
            res = FastDfsUtil().upload_by_buffer(update_user_obj.avatar_picture.read(), file_ext_name)
            if res['code'] == Constants.WEB_REQUEST_CODE_ERROR:
                return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.PIC_UPLOAD_ERROR}
            data = res['data']
            picture_url = Config.fdfs_nginx_ip + data['Remote file_id'].decode('utf-8')
            update_user_obj.avatar_url = picture_url
            update_user_obj.avatar_picture = None
        else:
            update_user_obj.avatar_url = None

        update_user_obj.sh_user_info_id = None
        update_dict = ObjToDict().obj_to_dict(update_user_obj)
        update_dict['update_time'] = int(time.time())
        # 更新对象属性
        """
        update_dict = {
            'sh_user_role_id': update_user_obj.sh_user_role_id,
            'email': update_user_obj.email,
            'telephone': update_user_obj.telephone,
            'nickname': update_user_obj.nickname,
            'avatar_url': update_user_obj.avatar_url,
            'update_time': int(time.time())
        }
        """

        print('update_dict---{}'.format(update_dict))
        try:
            update_res = UserInfo.objects.filter(id=user_obj.id, update_time=user_obj.update_time).update(
                **update_dict)

        except Exception as e:
            print('e--{}'.format(e))
            Logger().error('user_info_update_service-update:{}'.format(e), Constants.USER_MANAGE_LOG)
            if data:
                FastDfsUtil().delete(data['Remote file_id'])
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.DATA_UPDATE_ERROR}

        if not update_res:
            if data:
                FastDfsUtil().delete(data['Remote file_id'])
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.DATA_IS_CHANGED}

        # todo 删除原头像
        # if data:
            # print(origin_data['Remote file_id'])
            # FastDfsUtil().delete(origin_data['Remote file_id'])
        return {'code': Constants.WEB_REQUEST_CODE_OK, 'msg': Constants.DATA_UPDATE_OK}

    def user_info_update_password_service(self, user_info_obj):
        try:
            user_obj = UserInfo.objects.filter(id=user_info_obj.sh_user_info_id).first()

        except Exception as e:
            Logger().error('user_info_update_password_service-get:{}'.format(e), Constants.USER_MANAGE_LOG)

            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.SELECT_SQL_ERROR}

        if user_obj is None:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.OBJ_DELETE_IS_NOT_EXISTS}

        # 判断旧密码对不行
        old_password = self.sha_encryption.add_sha256(user_info_obj.old_password, SECRET_KEY)

        if old_password != user_obj.user_password:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.HAVE_ERROR_OLD_PASSWORD}

        new_password = self.sha_encryption.add_sha256(user_info_obj.new_password1, SECRET_KEY)

        try:
            update_res = UserInfo.objects.filter(id=user_obj.id, update_time=user_obj.update_time).update(
                user_password=new_password, update_time=int(time.time()))

        except Exception as e:
            Logger().error('user_info_update_password_service-update:{}'.format(e), Constants.USER_MANAGE_LOG)

            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.PASSWORD_UPDATE_ERROR}

        if not update_res:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.DATA_IS_CHANGED}

        return {'code': Constants.WEB_REQUEST_CODE_OK, 'msg': Constants.PASSWORD_UPDATE_OK}

    def user_info_reset_password_service(self, sh_user_info_id, request):
        # 先判断是否有权限重置密码
        role_name = request.user.sh_user_role_name

        if role_name not in [Constants.SUPPER_ADMIN, Constants.ADMIN]:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.NO_JURISDICTION_TO_OPERATION}

        try:
            user_obj = UserInfo.objects.filter(id=sh_user_info_id).first()

        except Exception as e:
            Logger().error('user_info_reset_password_service-get:{}'.format(e), Constants.USER_MANAGE_LOG)

            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.SELECT_SQL_ERROR}

        if user_obj is None:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.OBJ_DELETE_IS_NOT_EXISTS}

        new_password = self.sha_encryption.add_sha256(Constants.USER_ORIGIN_PASSWORD, SECRET_KEY)

        try:
            update_res = UserInfo.objects.filter(id=sh_user_info_id, update_time=user_obj.update_time).update(
                user_password=new_password, update_time=int(time.time()))

        except Exception as e:
            Logger().error('user_info_reset_password_service-update:{}'.format(e), Constants.USER_MANAGE_LOG)

            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.PASSWORD_UPDATE_ERROR}

        if not update_res:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.DATA_IS_CHANGED}

        return {'code': Constants.WEB_REQUEST_CODE_OK,
                'msg': '{}-新密码为:{}'.format(Constants.PASSWORD_RESET_OK, Constants.USER_ORIGIN_PASSWORD)}

    @transaction.atomic
    def user_app_authorization_service(self, auth_user_obj):
        # 查询到当前用户的对象
        try:
            user_obj = UserInfo.objects.filter(id=auth_user_obj.sh_user_info_id).first()

        except Exception as e:
            Logger().error('user_app_authorization_service-get:{}'.format(e), Constants.USER_MANAGE_LOG)

            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.SELECT_SQL_ERROR}

        if user_obj is None:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.OBJ_DELETE_IS_NOT_EXISTS}

        # 先获取到当前对象所有的关联关系--然后删除
        savepoint_id = transaction.savepoint()
        try:
            app_dict = {'id__in': auth_user_obj.sh_app_info_ids}
            apps_obj = AppInfoModel.objects.filter(**app_dict).all()

            user_obj.app_info.clear()
            user_obj.app_info.add(*apps_obj)

            transaction.savepoint_commit(savepoint_id)
            app_list = [{'id': one_app.id, 'app_name': one_app.app_name} for one_app in apps_obj]

            return {'code': Constants.WEB_REQUEST_CODE_OK, 'msg': Constants.USER_APP_AUTH_OK, 'data': app_list}
        except Exception as e:
            Logger().error('user_app_authorization_service-update:{}'.format(e), Constants.USER_MANAGE_LOG)

            transaction.rollback(savepoint_id)

            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.USER_APP_AUTH_ERROR}
