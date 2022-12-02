# coding=utf-8
from django.conf.urls import url
from auth_code_manage.views.auth_code_view import AuthCodeView

urlpatterns = [
    url(r'auth_code/', AuthCodeView.as_view()),
]
