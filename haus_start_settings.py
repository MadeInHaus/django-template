# This file will contain
# - a description of this project template
# - the list of variables to be substituted
# - the commands to be launched after copying the template files (e.g. git pull)

# Also, this file will NOT be copied
import os
from random import choice
from string import ascii_lowercase, digits
import stat
import json
import shutil
import fnmatch

def init_git():
    # Only init git if it isn't already there.
    if not os.path.exists('.git'):
        os.system("git init")

def get_replace_vars(no_prompt=False):
    defaults = {
        'PROJECT_NAME' : 'Haus Django Project',
        'ADMIN_EMAIL' : 'cms-admin@madeinhaus.com'
    }
    replace = {}

    # Take defaults from frontend package if available
    if os.path.exists('package.json'):
        with open('package.json') as fp:
            j = json.load(fp)
            config = j.get('config', {})
            defaults.update(config.get('vars', {}))

    for var, default in defaults.items():
        placemark = '__%s__' % var
        replace[placemark] = None
        help = var.replace('_', ' ')
        while not replace[placemark]:
            if no_prompt:
                replace[placemark] = default
            else:
                prompt = '%s [%s]: ' % (help, default)
                replace[placemark] = raw_input(prompt) or default

    # Always replace secret key
    key_seed = ''.join([choice(ascii_lowercase + digits) for x in range(50)])
    replace['__SECRET_KEY_SEED__'] = key_seed
    return replace

def replace_vars(replace, *base_dirs):
    # Only run replacement on files in project
    for d in base_dirs:
        for root, dirs, files in os.walk(d):
            DONT_REPLACE_IN = ['.svn', '.git',]
            for folder in DONT_REPLACE_IN:
                if folder in dirs:
                    dirs.remove(folder)
            for name in files:
                filepath = os.path.join(root, name)
                with open(filepath, 'r') as f:
                    data = f.read()
                for old_val, new_val in replace.items():
                    data = data.replace(old_val.encode('utf-8'), new_val.encode('utf-8'))
                with open(filepath, 'w') as f:
                    f.write(data)

def set_executables(base_dir):
    endswith = ('manage.py', 'post-receive', '.sh')
    for root, dirs, filenames in os.walk(base_dir):
        matches = []
        for filename in fnmatch.filter(filenames, '*.sh') + \
                        fnmatch.filter(filenames, 'manage.py') + \
                        fnmatch.filter(filenames, 'post-receive'):
            matches.append(os.path.join(root, filename))

        for f in matches:
            st = os.stat(f)
            perms = stat.S_IMODE(st.st_mode) | stat.S_IWUSR | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
            os.chmod(f, perms)

def concatenate_files(start):
    for filename in os.listdir(start):
        with open(filename, 'a') as fp:
            with open(os.path.join(start, filename)) as d:
                fp.write(d.read())
    shutil.rmtree(start)

def after_copy(no_prompt=False, no_git=False):
    if not no_git:
        init_git()

    # Replace variables with prompt values or defaults
    replace = get_replace_vars(no_prompt=no_prompt)
    replace_vars(replace, 'defaults', 'project')
    set_executables(os.getcwd())
    # Copy in default files
    concatenate_files('defaults')
