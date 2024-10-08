import os
import sys
import importlib
import jsonschema
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateError

from uip.constants import constants
from uip.utils import custom_io
from uip.exceptions import customexceptions
from uip.utils import formatting

from .. import package_dir


def copy_template(template_path, dst, keep_template_config=False):
    custom_io.copy_tree(template_path, dst)
    if not keep_template_config:
        template_config_yml = os.path.join(dst, constants.TEMPLATE_CONFIG_YAML)
        custom_io.remove_file(template_config_yml)


def copy_resources(resources_to_copy, dst):
    if resources_to_copy:
        resources_to_copy = [resources_to_copy] if type(
            resources_to_copy) == str else resources_to_copy
        resources_dir = os.path.join(package_dir, constants.RESOURCES_DIR)
        for resource in resources_to_copy:
            resource_path = os.path.join(resources_dir, resource)
            if os.path.isdir(resource_path):
                custom_io.copy_tree(resource_path, dst)
            elif os.path.isfile(resource_path):
                custom_io.copy_file(resource_path, dst)


def copy_setup_scripts(dst, scripts_to_copy=constants.SETUP_SCRIPTS_RESOURCES):
    if not os.path.exists(dst):
        raise customexceptions.FileNotFoundError(603, dst)
    elif type(scripts_to_copy) != list or len(scripts_to_copy) == 0 \
            or len(set(scripts_to_copy) - set(constants.SETUP_SCRIPTS_RESOURCES)) > 0:
        # 'scripts_to_copy' is either empty or contains an unknown item
        raise customexceptions.InvalidValueError(604,
            'scripts_to_copy ({})'.format(str(scripts_to_copy)),
            formatting.join_list_of_strings(constants.SETUP_SCRIPTS_RESOURCES, 'or'))

    copy_resources(scripts_to_copy, dst)


def get_setup_py_script_version(path_to_setup_py):
    if os.path.exists(path_to_setup_py) and os.path.isfile(path_to_setup_py) \
            and path_to_setup_py.endswith('.py'):
        version = None
        prev_sys_path = sys.path
        prev_sys_modules = sys.modules

        prev_stdout, prev_stderr = sys.stdout, sys.stderr

        try:
            sys.path = [os.path.dirname(path_to_setup_py)] + sys.path
            # [:-3] will remove '.py'
            module_name = os.path.basename(path_to_setup_py)[:-3]

            # Importing an older version of setup.py may result in output
            # being printed to stdout and stderr. To handle this, silence
            # stdout and stderr temporarily
            sys.stdout = sys.stderr = os.devnull

            setup = importlib.import_module(module_name)

            # Ensure the setup.py we imported is the one we expect
            if not hasattr(setup, '__file__') or \
                not os.path.samefile(setup.__file__, path_to_setup_py):
                raise ImportError()

            version = formatting.VersionInfo(str(setup.version_info()))

            # Remove 'module_name' from sys.modules
            if module_name in sys.modules:
                del sys.modules[module_name]
        except AttributeError:
            # Must be a newer setup.py, but cannot find version information
            version = None
        except SystemExit:
            # Must have the older setup.py which did not have
            # __name__ === '__main__', so it runs as soon as you import it
            version = None
        except Exception:
            # Some unknown and unexpected error occurred
            version = None
        finally:
            sys.stdout, sys.stderr = prev_stdout, prev_stderr

            sys.path.pop(0)
            if sys.path != prev_sys_path:
                raise SystemError('sys.path is corrupted')
            if sys.modules != prev_sys_modules:
                raise SystemError('sys.modules is corrupted')

        return version
    else:
        return None


def get_extension_template_details(template_path):
    if not template_path.endswith(constants.TEMPLATE_CONFIG_YAML):
        template_path = os.path.join(
            template_path, constants.TEMPLATE_CONFIG_YAML)
    if os.path.exists(template_path):
        template_details = custom_io.read_yaml(template_path)
        return template_details
    else:
        return None


# Returns an empty string if 'template_config' is valid else the error message
def validate_template_config(template_config):
    return formatting.validate_using_jsonschema(
        template_config,
        constants.VALID_TEMPLATE_CONFIG_SCHEMA)


def get_extension_templates(template_to_get=None):
    # if template_to_get is None, all templates will be retrieved

    uiptemplates = os.path.join(package_dir, 'uiptemplates')
    return_list = []
    if os.path.exists(uiptemplates):
        for template_folder in constants.TEMPLATE_FOLDERS:
            template_folder_path = os.path.join(uiptemplates, template_folder)
            if not os.path.exists(template_folder_path):
                continue

            extension_templates = [template for template in os.listdir(template_folder_path) if
                                   os.path.isdir(os.path.join(template_folder_path, template))]
            for extension_template in extension_templates:
                template_config_yml = os.path.join(template_folder_path,
                                                   extension_template, constants.TEMPLATE_CONFIG_YAML)

                if not os.path.exists(template_config_yml):
                    continue

                template_details = custom_io.read_yaml(template_config_yml)
                template_name = template_details.get('name', None)
                template_version = template_details.get('version', None)
                template_description = template_details.get(
                    'description', None)
                template_variables = template_details.get('variables', None)
                is_user_template = template_name not in constants.BUILT_IN_TEMPLATES

                if template_to_get is None:
                    return_list.append({
                        'template_name': template_name,
                        'template_version': template_version,
                        'template_description': template_description,
                        'template_variables': template_variables,
                        'template_path': os.path.join(template_folder_path, extension_template),
                        'is_user_template': is_user_template
                    })
                else:
                    parts = template_to_get.split(
                        constants.TEMPLATE_NAME_VERSION_SEPARATOR)
                    if len(parts) == 2:
                        # 'template_to_get' must be '<name>@<version>'
                        if parts[0] == template_name and parts[1] == template_version:
                            return_list.append({
                                'template_name': template_name,
                                'template_version': template_version,
                                'template_description': template_description,
                                'template_variables': template_variables,
                                'template_path': os.path.join(template_folder_path, extension_template),
                                'is_user_template': is_user_template
                            })
                    elif len(parts) == 1:
                        if parts[0] == template_name:
                            return_list.append({
                                'template_name': template_name,
                                'template_version': template_version,
                                'template_description': template_description,
                                'template_variables': template_variables,
                                'template_path': os.path.join(template_folder_path, extension_template),
                                'is_user_template': is_user_template
                            })

    return return_list


def get_all_extension_templates():
    return get_extension_templates()


def validate_jinja2_syntax(template_path, files_to_template):
    env = Environment(loader=FileSystemLoader(template_path),
                      keep_trailing_newline=True)
    for file_to_template in files_to_template:
        if not os.path.exists(os.path.join(template_path, file_to_template)):
            continue
        try:
            curr_template = env.get_template(file_to_template)
            env.parse(curr_template)
        except TemplateError as te:
            raise customexceptions.CorruptedFileError(323, file_to_template,
                                                      te.message)
