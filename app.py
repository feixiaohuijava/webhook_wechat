from flask import Flask, request, jsonify
import json
import requests
from tool import get_yaml_data
import logging

app = Flask(__name__)


@app.route('/api/webhook/one', methods=['POST'])
def hello_world():
    if request.data:
        data = json.loads(request.data.decode('utf-8'))
        app.logger.info(f"flask request data: {data}")
        receiver = data['receiver']
        status = data['status']
        alerts = data['alerts']
        yaml_data = get_yaml_data()
        if not yaml_data:
            return jsonify({"msg": "获取配置文件出错!"})
        alertnames_key = yaml_data['alertnames_key']

        labels_key = yaml_data['labels_key']
        status_key = yaml_data['status_key']
        webhook_url_key = yaml_data['webhook_url_key']

        alertname = alerts[0]["labels"]["alertname"]
        alertnames_zh_key = alertnames_key[alertname]
        wechat_heard = "监控指标名<font color='warning'>" + alertnames_zh_key + "</font>\n>"
        wechat_label = ""
        wechat_status = ""
        content = wechat_heard
        for each_alert in alerts:
            labels = each_alert['labels']
            annotations = each_alert['annotations']
            for each_labels_key in labels_key:
                wechat_label.join(each_labels_key + ":<font color='comment'>" + labels[each_labels_key] + "</font> \n>")
            for each_status_key in status_key:
                wechat_status.join(
                    each_status_key + ":<font color='comment'>" + annotations[each_status_key] + "</font> \n>")
            content = content.join(wechat_label).join(wechat_status)
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "content": content
            }
        }
        headers = {"Content-Type": "application/json"}
        requests.post(url=webhook_url_key, data=json.dumps(payload), headers=headers)
    return jsonify({"msg": "执行任务成功"})


if __name__ == '__main__':
    handler = logging.FileHandler('webhook_wechat.log')
    app.logger.addHandler(handler)
    app.run(debug=False, host='0.0.0.0', port='5000')
