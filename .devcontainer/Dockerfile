FROM python:3.10-alpine3.19

LABEL MAINTAINER = "Fedorov"

# 替换apk使用的源
COPY repositories /etc/apk/repositories
COPY requirements.txt /root/requirements.txt

# 设定容器时间
RUN echo "export TZ='UTC'" > /etc/profile

# Install required packages and remove the apk packages cache when done.
RUN apk --update --no-cache add python3-dev \
	g++ \
	pcre-dev \
	musl-dev \
	libxml2-dev \
	libxslt-dev \
	jpeg-dev

RUN pip3 install --no-cache-dir -r /root/requirements.txt

# 添加/root/.local/bin目录到环境变量
# ENV PATH="/root/.local/bin:${PATH}"
# RUN  rm -r /root/.cache

# 设置环境变量
ENV PYTHONPATH=/workspaces/liusu:$PYTHONPATH

EXPOSE 8899

CMD ["streamlit", "run", "auth.py", "--server.port 8899"]