#!/usr/bin/env python
# @desc :
__coding__ = "utf-8"
__author__ = "bytedance"

import time

import requests
import json
from wxauto import WeChat


def get_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """
    API_Key = ""
    Secret_Key = ""
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + API_Key + "&client_secret=" + Secret_Key + ""

    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")


def main(wx, msgs):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-speed-128k?access_token=" + get_access_token()

    for u in msgs.keys():
        for list_v in msgs[u]:
            # print(list_v)

            if list_v[0] == u:
                # print(list_v)
                payload = json.dumps({
                    "messages": [

                        {
                            "role": "user",
                            "content": list_v[1]
                        }
                    ]
                })
                headers = {
                    'Content-Type': 'application/json'
                }

                response = requests.request("POST", url, headers=headers, data=payload)
                json_result = json.loads(response.text)
                wx.SendMsg(msg=json_result['result'], who=u)

                # print(response.text)


if __name__ == '__main__':
    # 获取微信客户端
    wx = WeChat()

    # 指定发送信息
    user = "订阅号"
    # wx.SendMsg('你好，我在看着你。', user)
    # wx.ChatWith(user)

    while 1:

        # 获取所有新消息
        msgs = wx.GetAllNewMessage()
        # print(msgs.values())

        # 判断是否为空
        if msgs:
            main(wx, msgs)
            # print(msgs[-1].type)

        try:
            time.sleep(3.5)
            wx.ChatWith(user)
        except KeyboardInterrupt as e:
            wx.ChatWith(user)
            quit("退出。。。")
