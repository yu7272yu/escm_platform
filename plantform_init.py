import pymysql,sys, os, django
import re
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'escm_platform.settings')
django.setup()
from user_manage.models.user_info_model import UserInfoModel
from user_manage.models.user_role_model import UserRoleModel



from escm_platform.common.sha256_encryption import ShaEncryption
from escm_platform.common.constants import Constants
from escm_platform.settings import Config, SECRET_KEY

def mysql_db():
    print('开始创建数据库')
    db = pymysql.connect(
        host=  Config.mysql_host,  # 连接名称，默认127.0.0.1
        user= Config.mysql_user,  # 用户名
        passwd= Config.mysql_password ,  # 密码
        port= Config.mysql_port ,  # 端口，默认为3306
        charset='utf8mb4',  # 字符编码
    )
    cursor = db.cursor() #创建游标对象

    try:
        sql = 'show databases' 
        cursor.execute(sql)
        print('未创建数据库前：',cursor.fetchall()) #获取创建数据库前全部数据库

        dbname = Config.mysql_db
        sql = 'create database if not exists %s'%(dbname) #创建数据库
        cursor.execute(sql)

        sql = 'show databases' 
        cursor.execute(sql)
        print('创建新的数据库后：',cursor.fetchall()) #获取创建数据库后全部数据库
        # sql = 'drop database if exists %s'%(dbname) #删除数据库
        # cursor.execute(sql)
    except Exception as e:
        print('创建数据库失败：', e)
        db.rollback()  #回滚事务

    finally:
        cursor.close() 
        db.close()  #关闭数据库连接

def migrate_db():
    try:
        os.system('python3 manage.py makemigrations user_manage app_manage auth_code_manage' )
        os.system('python3 manage.py migrate' )
        db = pymysql.connect(
            host=  Config.mysql_host,  # 连接名称，默认127.0.0.1
            user= Config.mysql_user,  # 用户名
            passwd= Config.mysql_password ,  # 密码
            port= Config.mysql_port ,  # 端口，默认为3306
            charset='utf8mb4',  # 字符编码
            database=Config.mysql_db     #指定操作的数据库
        )
        cursor = db.cursor() #创建游标对象
        sql = 'show tables'
        cursor.execute(sql)
        tables = [cursor.fetchall()]
        table_ll = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_ll]
        print('显示创建的表:', table_list)  #显示创建的表

    except Exception as e:
        print('创建数据表异常:', e)  #显示创建的表
        db.rollback()  #回滚事务
    finally:
        cursor.close() 
        db.close()


def initial_data():
    try:
        print("开始创建数据")
        # 角色
        r1, r1_res = UserRoleModel.objects.get_or_create(role_name="超级管理员", data_status=Constants.DATA_IS_USED )
        r2, r2_res = UserRoleModel.objects.get_or_create(role_name="管理员", data_status=Constants.DATA_IS_USED )
        r2, r2_res = UserRoleModel.objects.get_or_create(role_name="普通用户", data_status=Constants.DATA_IS_USED )

        # 用户
        u_1={'user_name': 'root','sh_user_role_id': r1.id, 'data_status': Constants.DATA_IS_USED }
        user_1, u1_res = UserInfoModel.objects.get_or_create(**u_1)
        if u1_res:
            user_1.user_password = ShaEncryption().add_sha256('123456', SECRET_KEY)
            user_1.save()


        print("创建数据成功")

    except Exception as e:
        print("创建数据失败:", e)
        
        
if __name__ == '__main__':
    mysql_db()
    migrate_db()
    initial_data()
