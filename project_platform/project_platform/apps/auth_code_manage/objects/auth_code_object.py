# coding=utf-8


class AuthCodeObject(object):
    sh_authorization_code_id = None
    sh_app_info_ids = None
    app_names = None
    auth_code = None
    auth_company = None
    auth_project = None
    use_days = None
    resource_num = None
    auth_code_status = None
    remaining_time = None
    # 规避int类型不能为空
    start_time = None
    end_time = None
