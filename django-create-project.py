#!/usr/bin/env python3

import os
import fileinput

project = input("Enter short project name: ")

if os.path.isdir(project):
    print("ERROR: Project exists")
    exit()

os.mkdir(project)
os.chdir(project)
cmd = "virtualenv env -p `which python3` --prompt=[django-" + project + "]"
os.system(cmd)

# Install django with default packages
requirements = """django
flake8
autopep8
pytz
django-debug-toolbar
django-autofixture
"""
with open('requirements.txt', 'w+') as ouf:
    ouf.write(requirements)

os.system("env/bin/pip install -r requirements.txt")

# Initiate git repository
gitignore = """env
*.sqlite3
*_local*
*.pyc
__pycache__
*.rdb
*.log
log
static
"""
with open('.gitignore', 'w+') as ouf:
    ouf.write(gitignore)

os.system("git init && git add .gitignore && git commit -m 'Initial commit.'")

cmd = "env/bin/django-admin startproject " + project
os.system(cmd)

cmd = "mv " + project + " tmp && mv tmp/* . && rm -rf tmp"
os.system(cmd)

settings_new_lines = """    'autofixture',
    'debug_toolbar',
"""
settings_path = project + '/settings.py'
for line in fileinput.FileInput(settings_path, inplace=1):
    if "   'django.contrib.staticfiles'," in line:
        line = line.replace(line, line + settings_new_lines)
    print(line, end='')

os.system("git add . && git commit -m 'Install Django project.'")

# Output message
message = """

You can now type:
cd {0}
activate
"""
print(message.format(project))
