# coding=utf-8


class Config(object):
    """
    平台配置信息
    """

    # mysql 配置信息
    mysql_host = 'localhost'
    mysql_port = 3306
    mysql_user = 'root'
    mysql_password = '123456'
    mysql_db = 'escm'

    # reids配置信息
    redis_host = 'localhost'
    redis_port = 6379
    redis_library = 0
    
    # kafka配置信息
    kafka_host = '161.189.73.195'
    kafka_port = 9092

    # fdfs配置信息
    fdfs_host = False
    fdfs_nginx_ip = "http://161.189.73.195:8888/"
    fdfs_nginx_port = 8888


    #流媒体服务器相关
    zlm_url = "http://161.189.73.195"
    zlm_port = "8180"
    
    # 厂家
    manufacturer_name_list = ['海康威视', '大华', '宇视', '索尼', '安讯士', '博世', '寰旭']
    # 设备类型 
    machine_type_list = ['枪机', '球机', '半球', '小摄像头']
    # 阈值名称
    threshold_type_list = ['检测阈值', '违停时间阈值','限速阈值', '短信提示阈值', '删除阈值', '速度阈值', '人数阈值', '人车数量阈值', '人车停留时间阈值', '单位时间阈值', '变化量阈值']
