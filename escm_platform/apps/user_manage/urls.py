# coding=utf-8
from django.conf.urls import url
from user_manage.views.user_role_view import UserRoleView
from user_manage.views.user_info_view import UserInfoView
from user_manage.views.user_login_view import UserLoginView


urlpatterns = [
    url(r'user_role/', UserRoleView.as_view()),
    url(r'user_info/', UserInfoView.as_view()),
    url(r'user_login/', UserLoginView.as_view()),
]
