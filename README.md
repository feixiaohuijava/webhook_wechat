部署环境:
python3.7
centos 7

部署步骤:

1 pip install -r requirement

2 uwsgi.ini配置文件chdir,wsgi-file目录设置

3 uwsgi --ini uwsgi.ini