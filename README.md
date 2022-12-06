[toc]
# escm_platform

### 本地调试

#### 运行增强的 django shell：

```
python manage.py escm_platform/shell_plus
打印SQL:  --print-sql
```

#### 查找定义的urls
```
python3 escm_platform/manage.py show_urls
```
#### 调试断点
```
import pdb
pdb.set_trace()
```

<!-- 增加测试数据库容器 -->
docker run -d --name=mysql_test -p 3306:3306  -e MYSQL_ROOT_PASSWORD=123456 mysql:8.0.30

### docker调试

#### 服务启动情况下，生成库,表，数据
```
docker-compose exec app python escm_platform/plantform_init.py 
```

#### 运行增强的 django shell：

```
docker-compose exec app python escm_platform/manage.py shell_plus
打印SQL:  --print-sql
```

#### 查找定义的urls
```
docker-compose exec app python escm_platform/manage.py show_urls
```