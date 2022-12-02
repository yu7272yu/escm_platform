# coding=utf-8


class ObjToDict(object):
    def __init__(self):
        self.res_dict = {}

    def obj_to_dict(self, obj):
        key_list = [key for key in dir(obj) if
                    (not str(key).startswith('__') or not str(key).endswith("__")) and key not in ['limit', 'page']]

        for key in key_list:
            value_res = eval('obj.{}'.format(key))

            if value_res:
                self.res_dict[key] = value_res

        return self.res_dict
