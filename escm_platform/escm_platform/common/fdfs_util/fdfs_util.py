# coding=utf-8
import traceback

from escm_platform.common.logger import Logger
from escm_platform.common.constants import Constants
from fdfs_client.client import *

from config import Config


# todo------------需要完善的功能
class FastDfsUtil(object):
    """
    fast dfs 上传下载功能视图函数
    """

    def __init__(self):
        self.client_file = os.path.join(os.path.dirname(__file__), 'client.conf')
        print('self.client_file--{}'.format(self.client_file))

        self.tracker_conf = get_tracker_conf(self.client_file)
        self.client = self.create_client()

    def create_client(self):
        try:
            client = Fdfs_client(self.tracker_conf)
            return client
        except Exception as e:
            error_msg = 'create_client--{}'.format(Constants.FDFS_CREATE_FAIL.format(e, traceback.print_exc()))
            Logger().error(error_msg, Constants.FDFS_LOG)
            return None

    def download(self, file_name, file_id):
        """
        从Storage服务器下载文件
        :param file_name: String, 文件下载路径
        :param file_id: String, 待下载文件ID
        :return: dict {
            'Remote file_id'  : remote_file_id,
            'Content'         : local_filename,
            'Download size'   : downloaded_size,
            'Storage IP'      : storage_ip
        }
        """
        if not isinstance(file_id, bytes):
            file_id = bytes(file_id, 'UTF-8')
        try:
            ret_download = self.client.download_to_file(file_name, file_id)
            return {'code': Constants.WEB_REQUEST_CODE_OK, 'data': ret_download}
        except Exception as e:
            error_msg = 'download--{}'.format(Constants.FDFS_DOWNLOAD_FAIL.format(e, traceback.print_exc()))
            Logger().error(error_msg, Constants.FDFS_LOG)
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.FDFS_DOWNLOAD_FAIL}

    def download_to_buffer(self, file_id):
        """
        从Storage服务器获取文件的二进制流
        :param file_id: String, 待下载文件ID
        :return: dict {
            'Remote file_id'  : remote_file_id,
            'Content'         : file_buffer,
            'Download size'   : downloaded_size,
            'Storage IP'      : storage_ip
        }
        """
        if not isinstance(file_id, bytes):
            file_id = bytes(file_id, 'UTF-8')
        try:
            ret_download = self.client.download_to_buffer(file_id)
            return {'code': Constants.WEB_REQUEST_CODE_OK, 'data': ret_download}
        except Exception as e:
            error_msg = 'download_to_buffer--{}'.format(Constants.FDFS_DOWNLOAD_FAIL.format(e, traceback.print_exc()))
            Logger().error(error_msg, Constants.FDFS_LOG)
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.FDFS_DOWNLOAD_FAIL}

    def upload_by_filename(self, file_name):
        """
        上传文件到Storage服务器
        :param file_name: String, 文件上传路径
        :return: dict {
            'Group name'      : group_name,
            'Remote file_id'  : remote_file_id,
            'Status'          : 'Upload successed.',
            'Local file name' : local_file_name,
            'Uploaded size'   : upload_size,
            'Storage IP'      : storage_ip
        }
        """
        try:
            ret_upload = self.client.upload_by_filename(file_name)
            return {'code': Constants.WEB_REQUEST_CODE_OK, 'data': ret_upload}
        except Exception as e:
            error_msg = 'upload_by_filename--{}'.format(Constants.FDFS_UPLOAD_FAIL.format(e, traceback.print_exc()))
            Logger().error(error_msg, Constants.FDFS_LOG)
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.FDFS_UPLOAD_FAIL}

    def upload_by_buffer(self, file_buffer, file_ext_name='.png'):
        """
        上传文件到Storage服务器
        :param file_name: String, 文件上传路径
        :return: dict {
            'Group name'      : group_name,
            'Remote file_id'  : remote_file_id,
            'Status'          : 'Upload successed.',
            'Local file name' : local_file_name,
            'Uploaded size'   : upload_size,
            'Storage IP'      : storage_ip
        }
        """
        try:
            ret_upload = self.client.upload_by_buffer(file_buffer, file_ext_name)
            return {'code': Constants.WEB_REQUEST_CODE_OK, 'data': ret_upload}
        except Exception as e:
            error_msg = 'upload_by_buffer--{}'.format(Constants.FDFS_UPLOAD_FAIL.format(e, traceback.print_exc()))
            Logger().error(error_msg, Constants.FDFS_LOG)
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.FDFS_UPLOAD_FAIL}

    def delete(self, file_id):
        """
        从Storage服务器中删除文件
        :param file_id: String, 待删除文件ID
        :return: tuple ('Delete file successed.', remote_file_id, storage_ip)
        """
        if not isinstance(file_id, bytes):
            file_id = bytes(file_id, 'UTF-8')
        try:
            ret_delete = self.client.delete_file(file_id)
            return {'code': Constants.WEB_REQUEST_CODE_OK, 'data': ret_delete}
        except Exception as e:
            error_msg = 'delete--{}'.format(Constants.FDFS_DELETE_FAIL.format(e, traceback.print_exc()))
            Logger().error(error_msg, Constants.FDFS_LOG)
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.FDFS_DELETE_FAIL}

    def upload_by_buffer_request(self, request, file_buffer):
        file_ext_name = os.path.splitext(file_buffer.name)[1]
        res = FastDfsUtil().upload_by_buffer(file_buffer.read(), file_ext_name)
        if res['code'] == Constants.WEB_REQUEST_CODE_ERROR:
            return res['code'], res['msg'], None
        data = res['data']
        # 组装url
        # fdfs是否搭建在本机服务器
        if Config.fdfs_host:
            fdfs_nginx = 'http://' + request.get_host().split(':')[0] + ':' + Config.fdfs_nginx_port
        else:
            fdfs_nginx = Config.fdfs_nginx_ip
        picture_url = fdfs_nginx + data['Remote file_id'].decode('utf-8')
        remote_id = data['Remote file_id']

        return res['code'], picture_url, remote_id


if __name__ == '__main__':
    fdfs_worker = FastDfsUtil()
    file_name = os.path.join(os.path.dirname(__file__), '3.png')
    res = fdfs_worker.upload_by_filename(file_name)
    print(res)

    # res = fdfs_worker.download('test2.webp', 'group1/M00/00/00/rBuDzWLPsouAPhW_AABjMnW5uJE12.webp')
    # print(res)
    # print('res-type{}'.format(type(res)))
