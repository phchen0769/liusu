import time
import json
import requests
from requests.models import HTTPError

import body_create


# 利用企业ID和corps
# ecret构造request请求，获取access_token
def get_token():
    url = r"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=wxbb353bc082c14c99&corpsecret=LNxX01OozDxfKaXSu99twzeBNIK917aAIyS4UsgZGF8"

    # 构造数据包头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
    }
    # 发起get请求
    try:
        res = requests.get(url=url, headers=headers, verify=False)
        res.encoding = "utf-8"
        res_dis = json.loads(res.text)
        return res_dis["access_token"]
    except requests.HTTPError as e:
        print(e.errno)


# 利用url+access_token,提交学生数据
def info_send(access_token, body_json):
    # url+access_token拼接新的访问请求
    url = (
        r"https://qyapi.weixin.qq.com/cgi-bin/oa/applyevent?access_token="
        + access_token
    )

    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    }

    data = body_json.encode("utf-8")
    try:
        res = requests.post(url=url, data=data, headers=headers, verify=False)
        # 打印返回信息
        if res.status_code == 200:
            resJson = json.loads(res.text)
            if resJson["errcode"] == 0:
                return "发送成功！请返回企业微信中，请在企业微信关注审批状态变化"
            else:
                return f'错误代码：{resJson["errcode"]},错误原因：{resJson["errmsg"]}'
    except requests.HTTPError as e:
        return "网络错误。"


def main():
    # 生成access_token
    access_token = get_token()
    # access_token = "PwUOUcUozgN2cPAZNPEYZBN1F9kZ9nkZf9WVy3-wB7zNwb1tZNt7sYZELie71Qy_zPwYHqDfjjXt6kiZutnJcj7aYmhNc5iY8I5JC3fOKNw030VZfkgeBPje1qoRnvwxgXd2rWi2bVCWxqROLzneMmUGdi4Z3mMkWvdHuXk7Y_eExiinej96DkivplHqoFckoacBf5AMiDaCiXlf7Rceog"


if __name__ == "__main__":
    main()
    time.sleep(30)
