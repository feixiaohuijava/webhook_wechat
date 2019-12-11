from flask import Flask, request, jsonify
import json
import requests
import tool
import logging

app = Flask(__name__)
app.debug = True
handler = logging.FileHandler('webhook_wechat.log')
app.logger.addHandler(handler)


@app.route('/api/webhook', methods=['POST'])
def hello_world():
    yaml_data = tool.get_yaml_data()
    if not yaml_data:
        return jsonify({"msg": "获取配置文件出错!"})
    webhook_url_key = yaml_data['webhook_url_key']
    if request.data:
        try:
            data = json.loads(request.data.decode('utf-8'))
            app.logger.info(f"flask request data: {data}")
            receiver = data['receiver']
            status = data['status']
            alerts = data['alerts']
            if not isinstance(alerts, list):
                app.logger.error(f"alerts不是list,{alerts}")
            alertname = alerts[0]["labels"]["alertname"]
            if status == "firing":
                wechat_heard = "**" + status + "[" + str(
                    len(alerts)) + "]监控指标名**<font color='warning'>" + alertname + "</font>\n>"
                content_list = [wechat_heard]
                for each_alert in alerts:
                    labels = each_alert['labels']
                    wechat_label_list = []
                    wechat_status_list = []
                    for item in labels.keys():
                        wechat_label = item + ":<font color='info'>" + labels.get(item) + "</font> \n>"
                        wechat_label_list.append(wechat_label)
                    annotations = each_alert['annotations']
                    for item in annotations.keys():
                        wechat_status = item + ":<font color='comment'>" + annotations.get(item) + "</font> \n>"
                        wechat_status_list.append(wechat_status)
                    wechat_status_list.append("<font color='warning'>--------------------</font>\n")
                    each_alert_content = "".join(wechat_label_list + wechat_status_list)
                    content_list.append(each_alert_content)
                content = "".join(content_list)
            elif status == "resolved":
                wechat_heard = status + "监控指标名<font color='warning'>" + alertname + "</font>\n>"
                content = wechat_heard
            else:
                content = "异常状态:" + status
            payload = {
                "msgtype": "markdown",
                "markdown": {
                    "content": content
                }
            }
            headers = {"Content-Type": "application/json"}
            app.logger.info(payload)
            data = requests.post(url=webhook_url_key, data=json.dumps(payload), headers=headers)
            app.logger.info(data)
        except Exception as e:
            app.logger.error(e)
        return jsonify({"msg": "执行任务成功"})
    else:
        return jsonify({"msg": f"alertmanager传的参数为空"})
