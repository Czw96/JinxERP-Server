from pathlib import Path
import uuid


def run():
    create_nginx_config()
    create_django_config()
    create_gunicorn_config()


def create_nginx_config():
    is_need_create = input('是否需要创建 Nginx 配置文件吗? (y/n)\n')
    if is_need_create == 'y':
        listen_port = input('请输入 Nginx 监听端口:\n')
        server_port = input('请输入 Django 启动端口:\n')
        static_path = Path.cwd() / 'frontend/build/'

        with open('configs/nginx.conf', 'w') as file:
            file.write(f"""\
server {{
    listen {listen_port};
    charset utf-8;
    gzip_static on;

        location / {{
                root {static_path};
                index index.html index.html;
                try_files $uri $uri/ /index.html;
        }}

        location /api/ {{
                proxy_pass http://127.0.0.1:{server_port}/api/;
                proxy_pass_header Server;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_connect_timeout 3s;
                proxy_read_timeout 10s;
        }}

        location /media/images/ {{
                alias {Path.cwd()}/media/images/;
        }}

        location /media/files/ {{
                alias {Path.cwd()}/media/files/;
        }}
}}
""")


def create_django_config():
    is_production_environment = input('是否为生产环境? (y/n)\n')
    if is_production_environment == 'y':
        host = input('请输入服务器 IP 地址:\n')
        file_content = f"""\
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '{uuid.uuid4()}'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['{host}']

"""
    else:
        file_content = f"""\
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '{uuid.uuid4()}'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

"""

    host = input('请输入数据库 Host:\n')
    user = input('请输入数据库 User:\n')
    passowrd = input('请输入数据库 Passowrd:\n')
    database_name = input('请输入数据库名称:\n')

    file_content += f"""
# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {{
    'default': {{
        "ENGINE": "django.db.backends.postgresql",
        'HOST': '{host}',
        'PORT': '5432',
        'USER': '{user}',
        'PASSWORD': '{passowrd}',
        'NAME': '{database_name}',
    }}
}}
"""

    with open(Path.cwd() / 'configs/django.py', 'w') as file:
        file.write(file_content)


def create_gunicorn_config():
    is_need_create = input('是否需要创建 Gunicorn 配置文件吗? (y/n)\n')
    if is_need_create == 'y':
        server_port = input('请输入 Django 启动端口:\n')

        with open('configs/gunicorn.py', 'w') as file:
            file.write(f"""\
import multiprocessing


bind = '127.0.0.1:{server_port}'
workers = multiprocessing.cpu_count() * 2 + 1
reload = True
accesslog = 'logs/gunicorn.log'
access_log_format = '%(h)s %(t)s "%(r)s" %(s)s %(b)sB %(M)sms'
""")


if __name__ == '__main__':
    run()
