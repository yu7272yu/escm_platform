# coding=utf-8
import random
import string

import cv2
from django.http import StreamingHttpResponse

from escm_platform.common.base_view import BaseView
from django_redis import get_redis_connection
from escm_platform.common.constants import Constants
from user_manage.objects.user_info_object import UserObject
from user_manage.services.user_login_service import UserLoginService


class UserLoginView(BaseView):
    def __init__(self):
        self.redis_client = get_redis_connection("default")
        self.user_login_service = UserLoginService()

    def get_user_code(self, request):
        """
        随机生成登录验证码--登录页面请求数据
        :param request:
        :return:
        """
        # 限制请求频率
        user_ip = request.META['REMOTE_ADDR']

        limit_code_flag = '{}_code'.format(user_ip)
        now_num = self.redis_client.get(limit_code_flag)

        # 有值和没有值需要分开处理
        if now_num:
            # 数据值大于了限制次数
            if int(now_num) >= Constants.LOGIN_IP_LIMIT_NUM:
                return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.LOGIN_IP_LIMIT_MSG}
            # 在有效次数内  则新增即可
            else:
                self.redis_client.incr(limit_code_flag)
        # 当前ip没有请求标识--则直接新增且设置过期时长
        else:
            self.redis_client.incr(limit_code_flag)
            self.redis_client.expire(limit_code_flag, Constants.RANDOM_CODE_TIMEOUT)

        # 随机生成字符串
        code_str = ''.join(
            [random.choice(string.ascii_letters + string.digits) for i in range(Constants.RANDOM_CODE_NUM)])

        # 存储入redis
        self.redis_client.set(code_str.lower(), code_str, Constants.RANDOM_CODE_TIMEOUT)

        return {'code': Constants.WEB_REQUEST_CODE_OK, 'msg': Constants.WEB_REQUEST_MSG_OK, 'data': code_str}

    def user_login(self, request):
        user_name = request.POST.get('user_name')
        user_password = request.POST.get('user_password')
        user_code = request.POST.get('user_code')

        print('user_name-{}'.format(user_name))
        print('user_password-{}'.format(user_password))

        # todo--获取登录ip--如果1分钟内 当前ip登录超过3次 则不让登录
        user_ip = request.META['REMOTE_ADDR']

        if not all([user_name, user_password, user_code]):
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.HAVE_NO_ENOUGH_PARAMS}

        limit_login_flag = '{}'.format(user_ip)
        now_num = self.redis_client.get(limit_login_flag)

        # 有值和没有值需要分开处理
        if now_num:
            # 数据值大于了限制次数
            if int(now_num) >= Constants.LOGIN_IP_LIMIT_NUM:
                return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.LOGIN_IP_LIMIT_MSG}
            # 在有效次数内  则新增即可
            else:
                self.redis_client.incr(limit_login_flag)
        # 当前ip没有请求标识--则直接新增且设置过期时长
        else:
            self.redis_client.incr(limit_login_flag)
            self.redis_client.expire(limit_login_flag, Constants.RANDOM_CODE_TIMEOUT)

        # 校验验证码
        redis_code = self.redis_client.get(user_code.lower())

        if not redis_code:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.RANDOM_CODE_IS_TIMEOUT}

        if redis_code.decode('utf-8').lower() != user_code.lower():
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.RANDOM_CODE_IS_ERROR}

        # 验证码 校验后 则直接删除
        self.redis_client.delete(user_code.lower())
        # 校验账号名称和密码
        user_info_obj = UserObject()
        user_info_obj.user_name = user_name
        user_info_obj.user_password = user_password

        json_data = self.user_login_service.user_login_service(user_info_obj)

        return json_data

    def login_video(self, request):
        """
        视频流路由。将其放入img标记的src属性中。
        例如：<img src='https://ip:port/uri' >
        """
        # 视频处理
        video = cv2.VideoCapture(Constants.LOGIN_VIDEO_PATH)
        if not video.isOpened():
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.VIDEO_CAN_NOT_OPEN}
        # 使用流传输传输视频流
        return StreamingHttpResponse(self.gen_display(video), content_type='multipart/x-mixed-replace; boundary=frame')

    def gen_display(self, video):
        """
        视频流生成器功能。
        """
        while True:
            # 读取图片
            ret, frame = video.read()
            if ret:
                # 将图片进行解码
                ret, frame = cv2.imencode('.jpeg', frame)
                if ret:
                    # 转换为byte类型的，存储在迭代器中
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')

    def test(self, request):
        """
        视频流生成器功能。
        """
        return {'code': Constants.WEB_REQUEST_CODE_OK, 'msg': 'hello word'}

        
