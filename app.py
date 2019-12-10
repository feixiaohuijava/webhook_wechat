from flask import Flask, request
import json
import requests
app = Flask(__name__)


@app.route('/api/webhook/one', methods=['POST'])
def hello_world():
    print("start hello world")
    data = json.loads(request.data.decode('utf-8'))
    print(data)
    receiver_type = data['receive']
    labels = data['alerts']['labels']
    annotations = data['alert']['annotations']
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=2ea7dd9f-72c3-46fc-bd4e-e279a510dc3e"
    payload = {
    "msgtype": "markdown",
    "markdown": {
        "content": "实时新增用户反馈<font color='warning'>132例</font>，请相关同事注意。\n>类型:<font color=\"comment\">用户反馈</font> \n>普通用户反馈:<font color=\"comment\">117例</font> \n>VIP用户反馈:<font color=\"comment\">15例</font>"
    }
}
    headers = {"Content-Type": "application/json"}
    requests.post(url=url, data=json.dumps(payload), headers=headers)
    return "success"


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port='5000')
