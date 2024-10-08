import copy
import os
import platform
import subprocess
import sys
import uuid


def generate_uuid(remove_dashes=True):
    random_uuid = str(uuid.uuid4())
    return random_uuid.replace('-', '') if remove_dashes else random_uuid


def get_os_name():
    return platform.system().lower()


def deep_copy_dict(original_dict):
    return copy.deepcopy(original_dict)


def pip_install(path_to_requirements_txt, install_to):
    if os.path.exists(path_to_requirements_txt) and os.path.exists(install_to):
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', '-r', path_to_requirements_txt, '-t', install_to])


# Returns a generator that yields the values of all instances of 'key' in 'collection'
# Collection must be a 'dict'
def find_key(collection, key):
    if isinstance(collection, list):
        for item in collection:
            for val in find_key(item, key):
               yield val
    elif isinstance(collection, dict):
        if key in collection:
            yield collection[key]
        for item in collection.values():
            for val in find_key(item, key):
                yield val

# Updates all instances of 'key' in 'collection' with the value provided by
# 'value_func' function
def update_key(collection, key, value_func):
    if isinstance(collection, list):
        for item in collection:
            update_key(item, key, value_func)
    elif isinstance(collection, dict):
        if key in collection:
            collection[key] = value_func()
        for item in collection.values():
            update_key(item, key, value_func)

def git_clone(git_url, clone_in, branch_or_commit='', quiet=False):
    if git_url and clone_in:
        cmd = ['git', 'clone', git_url, clone_in]
        if quiet:
            cmd.append('-q')
        subprocess.check_call(cmd)

        if branch_or_commit:
            subprocess.check_call(['git', 'checkout', branch_or_commit], cwd=clone_in)
