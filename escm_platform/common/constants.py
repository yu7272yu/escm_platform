# coding=utf-8
import os


class Constants(object):
    """
    平台常理定义-规避魔法数字
    """

    # 【code 返回状态码定义】
    WEB_REQUEST_CODE_OK = 1
    WEB_REQUEST_CODE_ERROR = 0

    # 【API请求返回提升信息】
    WEB_REQUEST_MSG_OK = '请求成功'
    WEB_REQUEST_MSG_ERROR = '请求失败'
    HAVE_NO_ENOUGH_PARAMS = '参数不完整'
    DATA_ALREADY_EXISTS = '数据已存在'
    DATA_IS_NOT_EXISTS = '数据不存在'
    DATA_ADD_OK = '数据新增成功'
    DATA_ADD_ERROR = '数据新增失败'
    DATA_UPDATE_OK = '数据更新成功'
    DATA_UPDATE_ERROR = '数据更新失败'
    DATA_DELETE_OK = '数据删除成功'
    DATA_DELETE_ERROR = '数据删除失败'
    DATA_SYNCHRONIZATION_ERROR = '获取目标平台数据失败'
    OBJ_DELETE_IS_NOT_EXISTS = '数据操作对象不存在'
    USER_NAME_IS_EXISTS = '账户已存在'
    USER_APP_AUTH_ERROR = '用户应用授权更新失败'
    USER_APP_AUTH_OK = '用户应用授权更新成功'
    SELECT_SQL_ERROR = '数据查询异常'
    HAVE_NO_EXPECT_DATA = '暂无符合条件数据'
    TWO_TIME_TWO_PASSWORD = '两次密码不一致'
    HAVE_ERROR_OLD_PASSWORD = '旧密码不正确'
    PASSWORD_UPDATE_OK = '密码更新成功'
    PASSWORD_RESET_OK = '密码重置成功'
    PASSWORD_UPDATE_ERROR = '密码更新失败'
    APP_NAME_IS_ERROR = '应用名称异常'
    USER_INFO_ERROR = '用户信息异常'

    TOKEN_IS_NONE = 'token异常，未获取到token信息'
    TOKEN_ERROR_MSG = 'token异常，请重新登录'
    TOKEN_TIMEOUT_MSG = '登录超时，请重新登录'
    PASSWORD_ERROR_MSG = '账号或密码错误，请重新登录'
    DATA_IS_CHANGED = '待操作对象发生变化，请刷新页面稍后再试'
    PARAM_FORMAT_ERROR = '参数格式异常'

    IP_IS_ERROR = 'IP地址不正确'

    # 【系统设置有效时长】
    # 免登录 --token 有效数时长 单位天
    TOKEN_EXPIRE_DAYS = 100
    # 密码异操作次数5次 超过5次 需要10分钟后才能登录
    PASSWORD_ERROR_TIMES = 5
    PASSwORD_ERROR_LOCK_MINUTES = 10

    # 默认查询列表数据为空的返回字段
    DATA_NUM = 0
    DATA_DETAIL = []

    # 【日志名称定义】
    WEB_REQUEST_LOG = 'web_request.log'
    # 日志名称按照模块名称来
    ENTERPRISE_MANAGE_LOG = 'enterprise_manage.log'
    USER_MANAGE_LOG = 'user_manage.log'
    PRODUCT_MANAGE_LOG = 'product_manage.log'
    SYSTEM_MANAGE_LOG = 'system_manage.log'
    AUTH_CODE_MANAGE_LOG = 'auth_code_manage.log'
    PLAN_SCHEDULE_LOG = 'scheduler.log'
    KAFKA_MSG_LOG = 'kafka_msg.log'
    FDFS_LOG = 'fdfs.log'
    # 【授权码状态】
    # 授权码未激活
    AUTH_CODE_NO_ACTIVE = 2
    # 授权嘛已激活
    AUTH_CODE_IS_ACTIVE = 1
    # 授权码已过期
    AUTH_CODE_IS_EXPIRE = 0

    # app 授权应用列表--分为--平台授权 用户授权列表
    APP_AUTH_LIST_PLATFORM = 'platform_auth_flag'
    APP_AUTH_LIST_USER = 'user_auth_flag'

    # NO_ADD_AUTH_CODE_MSG = '已有未激活或未过期授权码,暂不能新增'
    NO_ADD_AUTH_CODE_MSG = '已存在授权码，暂不能新增'
    # 授权码激活提升信息
    AUTH_CODE_PROMPT_MSG = '访问受限，请激活或者更新授权码'
    NO_JURISDICTION_TO_OPERATION = '无操作权限'

    # 超级管理员账号
    SUPER_ADMIN_NAME = 'root'
    SUPER_ADMIN_NAME_IS_ERROR = '超级管理员账号错误'
    SUPPER_ADMIN = '超级管理员'
    ADD_SUPER_ADMIN_ROLE = '超级管理员角色不存在'
    ADMIN = '管理员'
    USER = '普通用户'

    # url路径请求函数下标层级
    URL_REQUEST_METHOD_INDEX = 3

    # 登录请求方法函数---当前请求不需要做token的验证-也不需要重写属性
    LOGIN_REQUEST_METHOD = 'user_login'
    LOGIN_CODE_METHOD = 'get_user_code'
    ADD_USER_ROLE_METHOD = 'user_role_add'
    SUPER_ADMIN_NAME_REGISTER = 'user_info_register'
    LOGIN_VIDEO_METHOD = 'login_video'
    MACHINE_RTSP_ACTION_METHOD = 'machine_rtsp_action'
    AUTH_CODE_INFO_METHOD = 'auth_code_info'

    # 不需要校验激活码请求方法函数 todo------------?
    NO_CHECK_AUTH_CODE_LIST = ['auth_code_update', 'auth_code_list', 'auth_code_info']

    # 数据表数据状态吗--有效1 无效0 逻辑删除字段
    DATA_IS_USED = 1
    DATA_IS_DELETED = 0

    FDFS_CREATE_FAIL = "FastDFS客户端创建失败, {0}, {1}"
    FDFS_DOWNLOAD_FAIL = "FastDFS文件下载失败, {0}, {1}"
    FDFS_UPLOAD_FAIL = "FastDFS文件上传失败, {0}, {1}"
    FDFS_DELETE_FAIL = "FastDFS文件删除失败, {0}, {1}"
    # FDFS_NGINX_IP = "http://192.168.100.225:80/"
    LOG_TEXT_FORMAT = "%(asctime)s %(threadName)s %(filename)s %(levelname)s %(message)s"
    LOG_DATE_FORMAT = "%Y/%m/%d %X"

    # 定义随机字符串长度 --
    RANDOM_CODE_NUM = 4
    # 随机字符串有效时间为60秒
    RANDOM_CODE_TIMEOUT = 60
    # 同一个ip 登录异常超过5次 则锁定10分钟能不让登录
    IP_LOCK_TIME = 600

    RANDOM_CODE_IS_TIMEOUT = '无效验证码或已过期'
    RANDOM_CODE_IS_ERROR = '验证码错误'

    # ip 登录频率限制--一分钟10次
    LOGIN_IP_LIMIT_NUM = 10
    LOGIN_IP_LIMIT_MSG = '操作过于频繁，请稍后再试'
    LOGIN_SUCCESS = '登录成功'
    USER_ORIGIN_PASSWORD = 123456

    # 阈值类型--属性格式 区间（范围） 唯一数值
    BETWEEN_TWO_NUM = 1
    BETWEEN_TWO_NUM_MSG = '区间范围'
    UNIQUE_ONE_NUM = 2
    UNIQUE_ONE_NUM_MSG = '唯一数值'
    THRESHOLD_TYPE_DICT = {
        BETWEEN_TWO_NUM: BETWEEN_TWO_NUM_MSG,
        UNIQUE_ONE_NUM: UNIQUE_ONE_NUM_MSG
    }

    # 区间测速最长时间1800秒
    MEASUREMENT_OUT_TIME = 1800

    # 系统配置阈值
    THRESHOLD_TO_SYSTEM = 1
    # 计划配置阈值
    THRESHOLD_TO_PLAN = 2
    # 叠加字符配置阈值
    THRESHOLD_TO_STRING = 3

    # 补充
    DATA_CHECK_OK = '1'
    DATA_CHECK_ERROR = '0'

    IP_FORMAT_ERROR = 'IP地址格式不正确'
    PORT_FORMAT_ERROR = '端口号格式不正确'
    LONGITUDE_LATITUDE_FORMAT_ERROR = '经纬度坐标格式不正确'
    REMOVE_FORMAT_ERROR = '是否为可动云台设备格式不正确'

    OVER_AUTH_CODE_RESOURCE_NUM = '设备录入数量超过了授权码规定数量上限'
    COORDINATE_NOT_MATCHING_RESOURCE = '线框类型与录入设备不匹配'
    COORDINATE_IS_EXISTS = '录入设备已存在线框'

    MACHINE_RESOURCE_HAVE_PLAN = '该设备存在计划，不能进行操作，请删除计划后尝试'
    MACHINE_RESOURCE_HAVE_APP = '该设备已被录入应用，不能进行操作，请移除应用后尝试'
    LIBRARY_HAVE_PLAN = '该图库存在计划，不能进行操作，请删除计划后尝试'

    MACHINE_TYPE_IS_NOT_EXISTS = '机型不存在'
    MANUFACTURER_IS_NOT_EXISTS = '厂家不存在'
    APP_IS_NOT_EXISTS = '应用不存在'
    MACHINE_RESOURCE_IS_NOT_EXISTS = '设备不存在'
    AUTH_CODE_IS_NOT_EXISTS = '授权码不存在'
    PLAN_IS_NOT_EXISTS = '计划不存在'
    LIBRARY_IS_NOT_EXISTS = '图库不存在'
    OBJ_UPDATE_IS_NOT_EXISTS = '数据更新对象不存在'
    PLAN_IS_NOT_NEW_VERSION = '当前计划不是最新版本'

    DATA_NOT_IN_APP = '数据不在应用中'
    MACHINE_RESOURCE_NOT_ENTRY_TO_APP = '设备未被录入应用中'
    MACHINE_RESOURCE_TIME_CONFLICT = '设备时间冲突'
    PLAN_IS_EXECUTE = '计划正在执行中，请暂停后尝试'
    APP_CAN_NOT_ADD_LIBRARY = '当前应用不能添加图库'
    PLAN_TIME_ERROR = '时间选择不正确'
    WEEK_ERROR = '计划执行星期不在选择时间范围内'

    PIC_UPLOAD_ERROR = '图片上传失败'
    PIC_DOWNLOAD_ERROR = '图片下载失败'
    PIC_DELETE_REMOTE_ERROR = '远端图片删除失败'
    THRESHOLD_ADD_ERROR = '阈值添加失败'

    DATA_ENTRY_OK = '录入成功'
    DATA_REMOVE_OK = '移除成功'
    # DATA_ADD_RENAME_OK = '数据新增成功，但新增数据为重名对象，名称为{}'
    DATA_LIST_ADD_MSG = '总共添加{}条数据,成功:{}条,失败:{}条'
    STREAMING_MEDIA_ADDR_GET_OK = '流媒体地址获取成功'
    STREAMING_MEDIA_ADDR_GET_ERROR = '未匹配厂家'

    PLAN_STATUS_CHANGE_OK = '计划状态改变成功'
    PLAN_START_OK = '计划开始成功'
    PLAN_STOP_OK = '计划暂停成功'

    IS_CLOCKWISE = '坐标为顺时针方向'
    NOT_IS_CLOCKWISE = '坐标为逆时针方向'

    MEMORY_ERROR_SAVE = '传入的图片错误'
    MEMORY_ERROR_DETECT =  '调用检测人脸detect接口失败'
    MEMORY_ERROR_DETECT_FACE =  '调用detect失败(没有人脸或者多张人脸)'
    MEMORY_ERROR_ALIGN =  '调用处理图片align接口失败'
    MEMORY_ERROR_EXTFEA = '调用获取图片特征值ext_fea接口失败'
    MEMORY_ERROR_FEA = '调用获取特征值异常'
    MEMORY_OK_UPLOAD =  '上传图片到内存中成功'
    MEMORY_ERROR_UPLOAD = '上传图片到内存中失败'
    MEMORY_OK_DELETE = '删除内存图片成功'
    MEMORY_ERROR_DELETE = '删除内存图片失败'
    MEMORY_ERROR_TASK_CREATE = '创建task失败'
    MEMORY_OK_TASK_CREATE = '创建task成功'
    MEMORY_ERROR_TASK_DELETE = '创建task失败'
    MEMORY_OK_TASK_DELETE = '创建task成功'
    MEMORY_ERROR_SEARCH = '调用查询人脸接口失败' 
    MEMORY_OK_SEARCH = '调用查询人脸接口成功'
    MEMORY_ERROR_HTTP_SEARCH = '调用查询人脸接口异常'
    MEMORY_OK_FEA_APPEND = '追加tag成功'
    MEMORY_ERROR_FEA_APPEND = '追加tag失败'


    # EXCEL表格相关设置
    IO_WRITE_ERROR = 'IO写入异常'
    EXCEL_HEAD_DATA_ERROR = '{} 表头数据不正确'
    EXCEL_ADD_ERROR_MSG = 'sheet:{sheet}, row:{row}: {error}'
    DELETE_ERROR_MSG = '数据id {id}删除失败, {error}'
    MACHINE_RESOURCE_SHEET = 'machine_resource_sheet'
    MACHINE_RESOURCE_EXCEL = 'machine_resource_excel'
    MACHINE_RESOURCE_BLANK_EXCEL = 'machine_resource_blank_excel'
    PLAN_RESULT_SHEET = 'plan_result_sheet'
    PLAN_RESULT_EXCEL = 'plan_result_excel'
    EXCEL_TYPE = '.xls'

    # 资源信息EXCEL表头
    MACHINE_RESOURCE_EXCEL_HEAD = ['设备名称', 'IP地址', '端口号', '账号', '密码', '经度', '纬度', '厂商', '机型', '是否为可动云平台', '流媒体地址']
    # 计划结果表头
    PLAN_RESULT_EXCEL_HEAD_TYPE_CAR = ['计划名称', '检测类型', '违法抓拍点', '抓拍时间', '车辆颜色', '车牌号', '抓拍图片']
    PLAN_RESULT_EXCEL_HEAD_TYPE_FACE = ['计划名称', '抓拍点名称', '时间', '照片']

    ILLEGAL_STOP = '违停'
    SPEED_MEASUREMENT = '区间测速'
    FACE_QUERY = '以脸搜脸'
    TRACK_QUERY = '轨迹查询'
    BLACK_LIST = '黑名单布控'
    WHITE_LIST = '白名单布控'
    FIRE_CHECK = '烟火检测'
    REGION_INTRUSION = '区域入侵'
    RUN_DETECTION = '奔跑检测'
    DIRECTION_DETECTION = '行进方向检测'

    COORDINATE_TYPE_ILLEGAL_STOP_CHECK_AREA = '违停检测区域'
    COORDINATE_TYPE_CAR_CHECK_AREA = '车辆检测区域'
    COORDINATE_TYPE_CHECK_SPEED_POINT = '测速点'
    COORDINATE_TYPE_CHECK_DIRECTION = '测速方向'
    COORDINATE_TYPE_CHECK_AREA = '检测区域'
    COORDINATE_TYPE_CHECK_DIRECTION_2 = '测速方向2'
    COORDINATE_TYPE_CHECK_AREA_2 = '检测区域2'
    COORDINATE_TYPE_DISTANCE_AREA = '标注距离'

    MATCHING_SIMILARITY_THRESHOLD_TYPE = '检测阈值'
    ILLEGAL_STOP_TIME_THRESHOLD_TYPE = '违停时间阈值'
    SPEED_LIMIT_THRESHOLD_TYPE = '限速阈值'
    SMS_PROMPT_TIME_THRESHOLD_TYPE = '短信提示阈值'
    DELETE_THRESHOLD_TYPE = '删除阈值'
    SPEED_THRESHOLD_TYPE = '速度阈值'
    PEOPLE_NUMBER_THRESHOLD_TYPE = '人数阈值'
    ALL_NUMBER_THRESHOLD_TYPE = '人车数量阈值'
    ALL_STOP_TIME_THRESHOLD_TYPE = '人车停留时间阈值'
    UNIT_TIME_THRESHOLD_TYPE = '单位时间阈值'
    CHANGE_NUMBER_THRESHOLD_TYPE = '变化量阈值'

    SMART_CAMERA = '小摄像头'
    SMART_CAMERA_CAN_NOT_OPERATION = '小摄像头不能进行相关操作'

    LOGIN_VIDEO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'login.mp4')
    VIDEO_CAN_NOT_OPEN = '视频播放错误'

    # 计划状态
    PLAN_STATUS_START = 1
    PLAN_STATUS_STOP = 0

    # 计划执行状态
    PLAN_EXE_STATUS_START = 1
    PLAN_EXE_STATUS_STOP = 0

    # 计划扫码时间间隔
    TEST_PLAN_SCAN_SECOND = 30

    # 计划最新版本标识
    NEW_VERSION_FLAG = 1
    NO_NEW_VERSION_FLAG = 0

    # 流媒体服务器相关
    ZLM_CLOSE_OK = "hls代理关闭成功"
    ZLM_ERROR = "调用流媒体服务器失败"

    # 操作flag --constants
    START_TEST_PLAN_FLAG = 'tset_plan_start'
    STOP_TEST_PLAN_FLAG = 'tset_plan_stop'

    # label as library
    LABEL_AS_LIBRARY = 1

    # 图片用途码
    PICTURE_FOR_RESULT = 2
    PICTURE_FOR_APP = 1
    PICTURE_FOR_PROCESS = 0

    # 前端线框大小
    COORDINATE_WIDTH = 780
    COORDINATE_LENGTH = 350

    # 告警信息是否已读
    ALARM_INFO_NOT_READ = 0
    ALARM_INFO_IS_READ = 1

    # 告警信息接收组群
    ALARM_INFO_GROUP = 'alarm_info_group_'

    MACHINE_NODE_MAX_NUMBER = 8
    MACHINE_NODE_OVERLAY = '创建失败，超过最大可创建点位数量'

    # 处理状态
    PROCESS_STATUS = {"created": 0, "processing": 1, "passed": 2}
    PROCESS_STATUS_NAME = {0: "报警", 1: "处理中", 2: "正常"}
    ALARM_TYPE = {"smoke": "烟雾报警", "fire": "火焰报警", "retrograde": "逆行", "gather": "聚集", "gather_linger": "聚集逗留", "increase": "剧增", "linger": "逗留"}


    # 方向
    DIRECTION_UP = 'up'
    DIRECTION_DOWN = 'down'
    DIRECTION_LEFT = 'left'
    DIRECTION_RIGHT = 'right'
    DIRECTION_FAR = 'far'
    DIRECTION_CLOSE = 'close'

    # 速度
    SPEED_UP = 0.2
    SPEED_DOWN = -0.2
    SPEED_LEFT = -0.2
    SPEED_RIGHT = 0.2
    DISTANCE_FAR = -0.05
    DISTANCE_CLOSE = 0.05

    PTZ_OK = '视频关闭成功'
    PTZ_ERROR = '获取视频帧失败'

    # 在算法平台Face中执行的任务id
    APP_NAME_IN_FACE_ALGORITHM = [FACE_QUERY, BLACK_LIST, WHITE_LIST]
    FACE_ALGORITHM = 'Face'

    # 在算法平台LPR中执行的任务id
    APP_NAME_IN_LPR_ALGORITHM = [SPEED_MEASUREMENT]
    LPR_ALGORITHM = 'LPR'

    # 在算法平台 Park 或者 ParkPTZ 中执行的任务id
    APP_NAME_IN_PARK_ALGORITHM = [ILLEGAL_STOP]
    PARK_ALGORITHM = 'Park'
    PARKPTZ_ALGORITHM = 'ParkPTZ'
    PARK_FLAG = 0
    PARKPTZ_FLAG = 1

    # 在算法平台FIRE中执行的任务id
    APP_NAME_IN_FIRE_ALGORITHM = [FIRE_CHECK]
    FIRE_ALGORITHM = 'Fire'

    # 在算法平台CHECK中执行的任务id
    APP_NAME_IN_CHECK_ALGORITHM = [DIRECTION_DETECTION, RUN_DETECTION, REGION_INTRUSION]
    CHECK_ALGORITHM = 'Check'

    ROAD_SECTION = {'nosection': 0, 'section': 1}
    ROAD_SECTION_NAME = {0: '非严选路段', 1: '严选路段'}

    # 是否为可动云平台 1: 是 2: 否
    REMOVE_MACHINE = 1
    NOT_REMOVE_MACHINE = 0

    # 需要判断是否为可动云平台的应用
    APP_JUDGE_REMOVE_MACHINE = [FIRE_CHECK, ILLEGAL_STOP, REGION_INTRUSION, RUN_DETECTION, DIRECTION_DETECTION]

    ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
