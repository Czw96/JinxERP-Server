import os
from pathlib import Path

project_path = Path.cwd()

# 删除 migrations 文件
print('删除 migrations 文件')
for app in (project_path / 'apps').iterdir():
    if app.is_file() or not (app / 'migrations').exists():
        continue

    for file in (app / 'migrations').iterdir():
        if file.is_file() and file.name != '__init__.py':
            file.unlink()


print('构建数据库')
os.chdir(project_path)
os.system('python manage.py makemigrations')
os.system('python manage.py migrate_schemas')
