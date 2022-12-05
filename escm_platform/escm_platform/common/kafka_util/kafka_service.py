# # coding=utf-8
# from cmath import e
# import json
# import time
# from kafka import KafkaProducer
# from kafka import KafkaConsumer
# from kafka.errors import kafka_errors
# import traceback
# from django.db import connections
# from concurrent.futures import ThreadPoolExecutor

# from app_manage.models.app_info_model import AppInfoModel
# from config import Config
# from plan_manage.models.plan_version_model import PlanVersionModel
# from plan_manage.models.test_plan_model import TestPlanModel
# from video_analysis_platform.common.logger import Logger
# from video_analysis_platform.common.constants import Constants
# from video_analysis_platform.apps.plan_manage.services.plan_result_service import PlanResultService
# from video_analysis_platform.apps.app_manage.services.picture_info_service import PicutrueInfoService
# from video_analysis_platform.apps.plan_manage.services.test_plan_service import TestPlanVersion



# # todo---
# class KafkaUtil(object):
#     def __init__(self):
#         self.plan_result_service = PlanResultService()
#         self.logger = Logger()
#         self.producer = KafkaProducer(
#             # value_serializer=lambda v: json.dumps(v).encode('utf-8'),
#             bootstrap_servers=['{}:{}'.format(Config.kafka_host, Config.kafka_port)],
#             api_version=(0, 10)
#         )
#         self.picture_info_service = PicutrueInfoService()
#         self.test_plan_version = TestPlanVersion()

#     def kafka_producer(self, topic, data):
#         future = self.producer.send(
#             topic,
#             value=json.dumps(data).encode(),
#             partition=0)  # 向分区1发送消息
#         self.logger.info('kafka_producer==>> topic:{}, data: {}'.format(topic, data), Constants.KAFKA_MSG_LOG)

#         try:
#             future.get(timeout=10)  # 监控是否发送成功

#         except kafka_errors[e] :  # 发送失败抛出kafka_errors
#             traceback.format_exc()

#     def kafka_consumer(self, topic):
#         info_msg = '开始消费数据--START_POLL_DATA'
#         self.logger.info(info_msg, Constants.PLAN_SCHEDULE_LOG)
#         consumer = KafkaConsumer(topic, bootstrap_servers='{}:{}'.format(Config.kafka_host, Config.kafka_port))

#         for msg in consumer:
#             data = msg.value.decode()
#             try:
#                 obj_dict = json.loads(data).get('object')
#                 self.logger.info('{}'.format(obj_dict), Constants.KAFKA_MSG_LOG)
#                 app_id = obj_dict.get('face').get('gender').split('&')[0]
#                 app_obj = AppInfoModel.objects.filter(id=app_id, data_status=Constants.DATA_IS_USED).first()
#                 if app_obj.app_name == Constants.SPEED_MEASUREMENT:
#                     self.plan_result_service.plan_result_add_car(obj_dict)
#                 elif app_obj.app_name == Constants.ILLEGAL_STOP:
#                     self.plan_result_service.plan_result_add_stop(obj_dict)
#                 # 人脸相关结果（以脸搜脸，黑名单，白名单）
#                 elif app_obj.app_name == Constants.FACE_QUERY or app_obj.app_name == Constants.BLACK_LIST or app_obj.app_name == Constants.WHITE_LIST:
#                     # 应用为以脸搜脸，应用码为结果 否为过程
#                     code = Constants.PICTURE_FOR_RESULT if app_obj.app_name == Constants.FACE_QUERY else Constants.PICTURE_FOR_PROCESS 
#                     # 本地存储人脸结果图片
#                     res, result_obj = self.plan_result_service.plan_result_add_face(obj_dict, code)
#                     self.logger.info(f"kafka_consumer-->> res:{res}, result_obj:{result_obj}", Constants.KAFKA_MSG_LOG)
#                     if res:
#                         # 传输消息到kafka以便于后期以脸搜脸的查询
#                         picture_obj = result_obj.sh_picture_info.all().first()
#                         # id: string  picture_used_code&picture的id&app_info_id&machine_resource_id&plan_version_id
#                         # 当图片是动态传入时
#                         id_str = '{}&{}&{}&{}&{}'.format(picture_obj.picture_used_code, picture_obj.id, result_obj.sh_app_info_id, result_obj.sh_machine_resource_id, result_obj.sh_plan_version_id)
#                         res_arr = [int(result_obj.sh_app_info_id), 100+int(result_obj.sh_machine_resource_id)]
#                         data = {
#                             'id': id_str,
#                             'tags': res_arr,
#                             'fea_url': picture_obj.picture_characteristic,
#                             'time': picture_obj.create_time
#                         }
#                         self.logger.info(f"kafka_consumer-->> data:{data}", Constants.KAFKA_MSG_LOG)
#                         # 推送到算法平台存储到内存中的kafka消息
#                         self.kafka_producer(Config.topic_algo_face_memory, data)
#                 elif app_obj.app_name == Constants.FIRE_CHECK:
#                     # 本地存储烟火检测结果图片
#                     res, result_obj = self.plan_result_service.plan_result_add_fire(obj_dict)
#                 elif app_obj.app_name in [Constants.RUN_DETECTION, Constants.DIRECTION_DETECTION, Constants.REGION_INTRUSION]:
#                     # 奔跑检测 or 行为方向检测 or 区域入侵
#                     res, result_obj = self.plan_result_service.plan_result_add_people(obj_dict)

#             except Exception as e:
#                 error_msg = 'kafka_consumer 数据存储异常--{}'.format(e)
#                 self.logger.error(error_msg, Constants.KAFKA_MSG_LOG)

#     def consumer_poll(self, topic):
#         info_msg = '开始拉取数据--START_POLL_DATA'
#         self.logger.info(info_msg, Constants.PLAN_SCHEDULE_LOG)
#         # 根据消费者topic创建消费者对象
#         consumer = KafkaConsumer(bootstrap_servers=['{}:{}'.format(Config.kafka_host, Config.kafka_port)])
#         consumer.subscribe(topics=(topic))

#         while True:
#             try:
#                 # 从kafka获取消息，每0.1秒拉取一次，单次拉取20条
#                 msg = consumer.poll(timeout_ms=100, max_records=1)
#             except Exception as e:
#                 error_msg = 'kafka_consumer 数据拉取异常--{}'.format(e)
#                 self.logger.error(error_msg, Constants.KAFKA_MSG_LOG)
#                 time.sleep(1)
#                 continue

#             # 数据正常拉取
#             for obj_1 in msg.values():
#                 try:
#                     # 获取到具体的数据---数据存储
#                     obj_dict = obj_1.values().decode()
#                     info_msg = '结果数据--{}'.format(obj_dict)
#                     self.logger.info(info_msg, Constants.KAFKA_MSG_LOG)
#                     app_id = obj_dict.get('face').get('gender').split('&')[0]
#                     app_obj = AppInfoModel.objects.filter(id=app_id, data_status=Constants.DATA_IS_USED)
#                     if app_obj.app_name == Constants.SPEED_MEASUREMENT:
#                         self.plan_result_service.plan_result_add_car(obj_dict)
#                     elif app_obj.app_name == Constants.FACE_QUERY:
#                         self.plan_result_service.plan_result_add_face(obj_dict)
#                     self.logger.info('add_success', Constants.KAFKA_MSG_LOG)
#                 except Exception as e:
#                     error_msg = 'kafka_consumer 数据存储异常--{}'.format(e)
#                     self.logger.error(error_msg, Constants.KAFKA_MSG_LOG)
#                     continue

#             time.sleep(1)

#     def smart_consumer(self, topic):
#         self.logger.info('开始消费小摄像头数据 --->> smart_consumer', Constants.PLAN_SCHEDULE_LOG)
#         consumer = KafkaConsumer(topic, bootstrap_servers='{}:{}'.format(Config.kafka_host, Config.kafka_port))

#         for msg in consumer:
#             data = msg.value.decode()

#             try:
#                 obj_dict = eval(json.loads(data))
#                 self.logger.info(f'obj_dict：{obj_dict}', Constants.PLAN_SCHEDULE_LOG)
#                 self.logger.info('{}'.format(obj_dict), Constants.KAFKA_MSG_LOG)
#                 self.picture_info_service.picture_info_add_service(obj_dict)
#                 self.logger.info('smart_consumer_add_success', Constants.KAFKA_MSG_LOG)

#             except Exception as e:
#                 error_msg = 'smart_consumer 数据存储异常--{}'.format(e)
#                 self.logger.error(error_msg, Constants.KAFKA_MSG_LOG)

#     def update_consumer(self, topic):
#         self.logger.info('开始消费黑白名单库结果数据 --->> update_consumer', Constants.KAFKA_MSG_LOG)
#         consumer = KafkaConsumer(topic, bootstrap_servers='{}:{}'.format(Config.kafka_host, Config.kafka_port))

#         for msg in consumer:
#             data = msg.value.decode()
#             try:
#                 obj_dict = json.loads(data)
#                 self.logger.info(f'update_consumer_obj_dict：{obj_dict}', Constants.KAFKA_MSG_LOG)
#                 self.picture_info_service.update_picture_used_code_service(obj_dict)
#                 self.logger.info('update_consumer_add_success', Constants.KAFKA_MSG_LOG)

#             except Exception as e:
#                 error_msg = 'update_consumer 数据存储异常--{}'.format(e)
#                 self.logger.error(error_msg, Constants.KAFKA_MSG_LOG)

#     def error_catch(self, topic):
#         self.logger.info('开始消费捕获视频源错误异常 -->> error_catch', Constants.KAFKA_MSG_LOG)
#         consumer = KafkaConsumer(topic, bootstrap_servers='{}:{}'.format(Config.kafka_host, Config.kafka_port))

#         for msg in consumer:
#             data = msg.value.decode()
#             try:
#                 self.logger.info(f"error_catch -->> data: {data} ", Constants.KAFKA_MSG_LOG)
#                 # 任务开始拼接id_str: app_info_id$plan_version_id&machine_resource_id$
#                 id = json.loads(data).get('id')
#                 msg = json.loads(data).get('message')
#                 self.logger.info(f"error_catch -->> id: {id} ", Constants.KAFKA_MSG_LOG)
#                 plan_version_id = id.split('&')[1]
                
#                 # 获取到对应的计划对象状态更改为关闭
#                 plan_version_obj = PlanVersionModel.objects.filter(id=plan_version_id).first()
#                 if plan_version_obj is None:
#                     self.logger.info('error_catch -->> 数据库查询异常-{}'.format(plan_version_id), Constants.KAFKA_MSG_LOG)
#                     continue
#                 plan_obj = plan_version_obj.sh_test_plan
#                 self.logger.info('error_catch -->> sh_test_plan : exe_status: {}'.format(plan_obj.exe_status), Constants.KAFKA_MSG_LOG)
#                 if plan_obj.exe_status == Constants.PLAN_EXE_STATUS_STOP:
#                     # todo 如果计划执行状态为未执行，休眠1秒
#                     time.sleep(1)
#                 plan_obj.exe_status = Constants.PLAN_EXE_STATUS_STOP
#                 plan_obj.save()
#                 self.logger.info('error_catch -->> sh_test_plan_exe_status: {}'.format(plan_obj.exe_status), Constants.KAFKA_MSG_LOG)

#                 # 关闭检索服务器的task
#                 self.test_plan_version.delete_http_task(plan_version_id)
#                 self.logger.info('error_catch -->> {}视频播放异常:{}'.format(id, msg), Constants.KAFKA_MSG_LOG)
#             except Exception as e:
#                 error_msg = 'error_catch 数据存储异常--{}'.format(e)
#                 self.logger.error(error_msg, Constants.KAFKA_MSG_LOG)

#     def kafka_run(self):
#         info_msg = '计划结果后台存储开始启动--START_KAFKA_CONSUMER'
#         self.logger.info(info_msg, Constants.PLAN_SCHEDULE_LOG)

#         with ThreadPoolExecutor(5) as t_pools:
#             for i in range(5):
#                 if i == 0:
#                     # 启动人脸消费topic
#                     t_pools.submit(self.kafka_consumer, Config.topic_algorithm_face)
#                 if i == 2:
#                     # 小摄像头消费topic
#                     t_pools.submit(self.smart_consumer, Config.topic_smart_face)

#                 if i == 3:
#                     # 视频源异常信息消费topic
#                     t_pools.submit(self.error_catch, Config.topic_error_msg)
                    
#                 if i == 4:
#                     # 获取黑白名单库结果消费topic
#                     t_pools.submit(self.update_consumer, Config.topic_algo_update_memory)
            
#         t_pools.shutdown(wait=True)


# if __name__ == '__main__':
#     worker = KafkaUtil()
#     worker.kafka_run()
#     # worker.consumer_poll('text1')
