import os

import app

import yaml


def get_yaml_data():
    try:
        yaml_file = os.path.join(app.app.root_path, 'config', 'webhook.yaml')
        yaml_data = yaml.load(open(yaml_file), Loader=yaml.FullLoader)
    except Exception as e:
        app.logger.error(f"读取webhook.yaml配置文件出错,原因: {str(e)}")
        return None
    alertnames_key = yaml_data['webhook']['alertnames']
    labels_key = yaml_data['webhook']['labels']
    status_key = yaml_data['webhook']['status']
    webhook_url_key = yaml_data['webhook']['webhook_url']
    return {"alertnames_key": alertnames_key, "labels_key": labels_key, "status_key": status_key,
            "webhook_url_key": webhook_url_key}


if __name__ == '__main__':
    data = get_yaml_data()
    print(data)