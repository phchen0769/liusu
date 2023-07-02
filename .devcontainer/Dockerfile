FROM mcr.microsoft.com/devcontainers/python:0-3.11

LABEL MAINTAINER = "Fedorov"

COPY requirements.txt /root/requirements.txt

RUN pip3 install --upgrade pip && pip3 config set global.index-url https:\/\/pypi.tuna.tsinghua.edu.cn\/simple
RUN pip3 install -r /root/requirements.txt

EXPOSE 8888

CMD ["streamlit", "run", "auth.py", "--server.port 8888"]