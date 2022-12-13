FROM silverlogic/python3.8

RUN apt-get update --fix-missing && \
    apt-get -y install iputils-ping  && \
    apt-get install vim -y && \
    apt-get install net-tools && \
    python -m pip install --upgrade pip

# 设置工作区
RUN mkdir /project_platform
WORKDIR /project_platform
# 导入环境
ADD ./project_platform/requirement.txt /project_platform
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirement.txt --no-cache-dir

# COPY ./project_platform/. .