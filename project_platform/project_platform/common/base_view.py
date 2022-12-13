# coding=utf-8
from django.views.generic import View
from django.http import JsonResponse
from project_platform.common.constants import Constants
from project_platform.common.jwt_token import JwtToken
from project_platform.common.logger import Logger


class BaseView(View):
    def __init__(self):
        pass

    # @JwtToken.auth_token
    def get(self, request):
        json_data = self.__handle_request(request)

        # get 请求也可能是数据流
        if isinstance(json_data, dict):
            return JsonResponse(json_data, safe=False, json_dumps_params={"ensure_ascii": False})

        return json_data

    # @JwtToken.auth_token
    def post(self, request):
        json_data = self.__handle_request(request)
        return JsonResponse(json_data, safe=False, json_dumps_params={"ensure_ascii": False})

    # @JwtToken.auth_token
    def delete(self, request):
        json_data = self.__handle_request(request)
        return JsonResponse(json_data, safe=False, json_dumps_params={"ensure_ascii": False})

    # @JwtToken.auth_token
    def put(self, request):
        json_data = self.__handle_request(request)
        return JsonResponse(json_data, safe=False, json_dumps_params={"ensure_ascii": False})

    def __handle_request(self, request):
        path = request.path
        Logger().debug(path, Constants.WEB_REQUEST_LOG)
        method_name = path.split('/')[Constants.URL_REQUEST_METHOD_INDEX]

        try:
            json_data = self.__getattribute__(method_name)(request)

        except Exception as e:
            json_data = {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': "{}".format(e)}
            Logger().error('web请求:{}-异常:{}'.format(path, e), Constants.WEB_REQUEST_LOG)

        return json_data
