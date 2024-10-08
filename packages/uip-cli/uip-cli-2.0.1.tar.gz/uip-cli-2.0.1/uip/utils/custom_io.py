import glob
import hashlib
import json
import os
import shutil
import tempfile
import io
import zipfile
import stat
from distutils import dir_util

import yaml


def read_yaml(filepath):
    if os.path.exists(filepath):
        with io.open(filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    else:
        return None


def read_json(filepath):
    if os.path.exists(filepath):
        with io.open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return None


def read_user_input(prompt):
    try:
        input_prompt = raw_input
    except NameError:
        input_prompt = input

    return input_prompt(prompt)


def read_user_choice(message, choice_list):
    if not choice_list or len(choice_list) == 0:
        return None

    print(message)
    for index, value in enumerate(choice_list):
        print(('  (%d) %s' % ((index + 1), value)))
    print('')

    user_choice = -1
    while user_choice < 1 or user_choice > len(choice_list):
        user_choice = read_user_input(
            'Please type the number of one of the choices presented above: ')
        try:
            user_choice = int(user_choice)
        except ValueError:
            user_choice = -1
            pass

    return choice_list[user_choice - 1]


def get_most_recent_file(dir, filetype='*'):
    if dir and os.path.exists(dir):
        if not filetype.startswith('*.'):
            filetype = '*.%s' % filetype
        files = glob.glob(os.path.join(dir, filetype))
        return max(files, key=os.path.getctime) if files else None
    else:
        return None


def get_files_of_specific_type(dir, filetype):
    if os.path.exists(dir):
        if not filetype.startswith('*.'):
            filetype = '*.%s' % filetype
        return glob.glob(os.path.join(dir, filetype))
    else:
        return None


def get_md5_of_zipfile(zip_filepath):
    if zip_filepath and os.path.exists(zip_filepath) and zipfile.is_zipfile(zip_filepath):
        md5 = hashlib.md5()
        with zipfile.ZipFile(zip_filepath, 'r') as zf:
            for f in zf.infolist():
                md5.update(str(f.CRC).encode('utf-8'))
        return md5.hexdigest()
    else:
        return None


def get_md5_of_file(filepath):
    if filepath and os.path.exists(filepath):
        md5 = hashlib.md5()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5.update(chunk)
        return md5.hexdigest()
    else:
        return None


def extract_zip(zip_filepath, extract_dir):
    with zipfile.ZipFile(zip_filepath, 'r') as zf:
        zf.extractall(extract_dir)


def remove_dir(dir):
    if os.path.exists(dir):
        def handle_error(func, path, exec_info):
            os.chmod(path, stat.S_IWUSR)

            try:
                func(path)
            except Exception as ex:
                raise

        shutil.rmtree(dir, False, handle_error)


def remove_file(file):
    if os.path.exists(file):
        os.remove(file)


def copy_tree(src, dst):
    if os.path.exists(src):
        dir_util._path_created = {}
        dir_util.copy_tree(src, dst)


def copy_file(src, dst):
    if os.path.exists(src) and os.path.isfile(src):
        shutil.copy(src, dst)


def write_to_file(dst_file, contents):
    with io.open(dst_file, 'wb+') as f:
        f.write(contents.encode('utf-8'))


def make_dir(dirpath):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)


def get_dir_listing(dirpath):
    if os.path.exists(dirpath):
        dir_listing = []
        for path, _, files in os.walk(dirpath):
            for name in files:
                dir_listing.append(os.path.join(path, name))

        return dir_listing
    else:
        return []


def get_zip_listing(zip_filepath):
    if not os.path.exists(zip_filepath):
        return []

    try:
        with zipfile.ZipFile(zip_filepath, 'r') as z:
            return z.namelist()
    except zipfile.error:
        return []


def get_temp_dir(prefix=None):
    return tempfile.mkdtemp(prefix=prefix)


def zip_directory(filename, dirpath, include_parent=False):
    if not os.path.exists(dirpath) or len(os.listdir(dirpath)) == 0:
        return False

    def zipdir(path, zip_handle):
        for root, _, files in os.walk(path):
            for f in files:
                zip_handle.write(os.path.join(root, f),
                        os.path.relpath(os.path.join(root, f),
                        os.path.join(path, '..') if include_parent else path))

    if not filename.endswith('.zip'):
        filename += '.zip'

    with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipdir(dirpath, zipf)

    return True