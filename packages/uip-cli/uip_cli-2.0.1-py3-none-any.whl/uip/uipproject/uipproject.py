import os
from subprocess import CalledProcessError
import zipfile
import json
import re
import requests

from setuptools import sandbox
from uip.constants import constants
from uip.exceptions import customexceptions
from uip.uiptemplates import template
from uip.utils import custom_io, formatting, generic

from .. import package_dir, UIP_CLI_VERSION


def is_valid_extension_template_dir(dir, require_setup_files=True):
    if not os.path.exists(dir):
        return False

    if require_setup_files:
        valid_extension_template_files = constants.VALID_EXTENSION_TEMPLATE_FILES
    else:
        valid_extension_template_files = constants.VALID_EXTENSION_TEMPLATE_FILES_WITHOUT_SETUP

    for f in valid_extension_template_files:
        if not os.path.exists(os.path.join(dir, f)):
            return False

    return True


def is_valid_dot_uip_dir(dir):
    config_file_path = os.path.join(dir, constants.DOT_UIP_FOLDER_NAME, constants.CONFIG_FILE_DIR_NAME,
                                    constants.CONFIG_FILE_NAME)
    return os.path.exists(config_file_path)


def is_valid_dot_uip_and_extension_template_dir(dir, require_setup_files=True):
    return is_valid_extension_template_dir(dir, require_setup_files) and is_valid_dot_uip_dir(dir)


def create_dot_uip_dir(dir, overwrite=False):
    if overwrite or not is_valid_dot_uip_dir(dir):
        dst_config_file_dir = os.path.join(dir, constants.DOT_UIP_FOLDER_NAME, constants.CONFIG_FILE_DIR_NAME)
        custom_io.make_dir(dst_config_file_dir)

        config_file_dir = os.path.join(package_dir, constants.CONFIG_FILE_DIR_NAME)
        variables = {'UIP_CLI_VERSION': UIP_CLI_VERSION}
        rendered_config_file = formatting.jinja_render_file(config_file_dir, constants.CONFIG_FILE_NAME, variables)
        custom_io.write_to_file(os.path.join(dst_config_file_dir, constants.CONFIG_FILE_NAME), rendered_config_file)


def process_user_specified_template(user_specified_template, folder_to_save_in):
    success = True

    if user_specified_template.startswith('git+'):        
        url = user_specified_template[4:] # everything after "git+"

        if len(url) == 0:
            raise customexceptions.InvalidValueError(318)

        groups = re.findall(constants.GIT_BRANCH_COMMIT_TAG_REGEX,
            url)
        # groups should be [(branch/commit/tag, branch/commit/tag value)] if the
        # user specified a branch/commit/tag

        branch_commit_tag = ""
        if len(groups) == 1 and len(groups[0]) == 2:
            # User specified a branch/commit/tag
            branch_commit_tag = groups[0][1]
            # Update the url to no longer contain "@branch/@commit/@tag"
            url = url[0:url.index("@"+groups[0][0])]

        try:
            generic.git_clone(url, folder_to_save_in, branch_commit_tag)
        except CalledProcessError:
            print('=' * 88)
            raise customexceptions.InvalidValueError(318)
        finally:
            # Delete the '.git' folder
            custom_io.remove_dir(os.path.join(folder_to_save_in, '.git'))
        print('=' * 88)
    elif user_specified_template.startswith('http://') or user_specified_template.startswith('https://'):
        response = requests.get(user_specified_template, stream=True)
        if response.ok:
            content_type = response.headers.get('Content-Type', None)
            if not content_type or content_type not in constants.ZIP_CONTENT_TYPES:
                raise customexceptions.CorruptedFileError(320)

            filename = response.headers.get('Content-Disposition', 'usertemplate.zip')
            fullpath = os.path.join(folder_to_save_in, filename)

            with open(fullpath, 'wb') as f:
                f.write(response.content)

            listing = custom_io.get_zip_listing(fullpath)
            if not listing or not constants.VALID_USER_EXTENSION_TEMPLATE_FILES.issubset(set(listing)):
                # must be an invalid zip file
                raise customexceptions.CorruptedFileError(320)
            
            custom_io.extract_zip(fullpath, folder_to_save_in)
            custom_io.remove_file(fullpath)
        else:
            raise customexceptions.InvalidValueError(319, response.status_code,
                response.reason)
    elif user_specified_template.endswith('.zip'):
        if not os.path.exists(user_specified_template):
            raise customexceptions.FileNotFoundError(313, user_specified_template)

        listing = custom_io.get_zip_listing(user_specified_template)
        if not listing or not constants.VALID_USER_EXTENSION_TEMPLATE_FILES.issubset(set(listing)):
            # must be an invalid zip file
            raise customexceptions.CorruptedFileError(311, user_specified_template)

        # zip file contains all the expected files.
        # Extract to a temporary folder
        custom_io.extract_zip(user_specified_template, folder_to_save_in)
    else:
        success = False

    return success


def save_user_specified_template(template_path, template_details=None):
    if not template_path:
        return

    user_templates_dir = os.path.join(package_dir, constants.USER_TEMPLATES_PATH)
    custom_io.make_dir(user_templates_dir) # creates '_usertemplates_' folder

    if template_details is None:
        template_config_yml = os.path.join(template_path, constants.TEMPLATE_CONFIG_YAML)
        template_details = custom_io.read_yaml(template_config_yml)

    template_version = formatting.replace_nonalphanum_chars(
        template_details['version'].lower())

    template_to_save_dir = os.path.join(user_templates_dir,
        '%s_%s' % (template_details['name'], template_version))

    updating_template = os.path.exists(template_to_save_dir)

    custom_io.remove_dir(template_to_save_dir) # if the template already exists, delete it
    custom_io.make_dir(template_to_save_dir)
    template.copy_template(template_path, template_to_save_dir,
        keep_template_config=True)

    return (template_details['name'], template_details['version'], updating_template)


def initialize_uip(starter_template_name, variables, dir, save):
    if starter_template_name is None:
        # attempt to initialize an empty repository
        if is_valid_extension_template_dir(dir, require_setup_files=False):
            if not is_valid_dot_uip_dir(dir):
                create_dot_uip_dir(dir)
                for setup_file in constants.SETUP_SCRIPTS_RESOURCES:
                    setup_file_name = os.path.basename(setup_file)
                    if not os.path.exists(os.path.join(dir, setup_file_name)):
                        template.copy_setup_scripts(dir)
                        break
                return 'Successfully created %s folder in "%s"' % (constants.DOT_UIP_FOLDER_NAME, dir)
            else:
                raise customexceptions.InitError(303, constants.DOT_UIP_FOLDER_NAME, dir)
        else:
            raise customexceptions.InvalidFolderError(308, dir)
    else:
        try:
            template_path = None
            temp_folder = custom_io.get_temp_dir(prefix=constants.TEMP_DIRECTORY_PREFIX)
            is_user_template = True

            success = process_user_specified_template(starter_template_name, temp_folder)
            
            if success:
                template_path = temp_folder
            else:    
                extension_template = template.get_extension_templates(starter_template_name)
                if not extension_template:
                    raise customexceptions.InvalidValueError(311, starter_template_name)
                elif len(extension_template) > 1:
                    # Found multiple templates. Need version to differentiate
                    raise customexceptions.InitError(316, formatting.join_list_of_strings(
                        list(map(lambda t: t['template_version'], extension_template)), 'or'))
                template_path = extension_template[0].get('template_path')
                is_user_template = False

            if is_valid_dot_uip_and_extension_template_dir(dir):
                raise customexceptions.InitError(307, dir)

            template_details = template.get_extension_template_details(template_path)

            if template_details is None:
                # 'template_config.yml' must not exist
                raise customexceptions.FileNotFoundError(313, constants.TEMPLATE_CONFIG_YAML)

            # validate 'template_config.yml'
            error = template.validate_template_config(template_details)
            if error:
                raise customexceptions.CorruptedFileError(314,
                            constants.TEMPLATE_CONFIG_YAML, error)

            template_name = template_details['name']
            if is_user_template and template_name in constants.BUILT_IN_TEMPLATES:
                raise customexceptions.InvalidValueError(315,
                    formatting.join_list_of_strings(constants.BUILT_IN_TEMPLATES,
                        'or'))        

            files_to_template = template_details.get('files_to_template', [])

            # ensure 'files_to_template' have correct jinja2 syntax
            template.validate_jinja2_syntax(template_path, files_to_template)

            variable_dict = {}
            for var_name, var_details in template_details.get('variables', {}).items():
                variable_dict[var_name] = var_details['default']

            if variables:
                variable_dict.update(variables)

            create_dot_uip_dir(dir, overwrite=True)

            if is_valid_dot_uip_dir(dir):
                template.copy_setup_scripts(dir)

                # Copying the template last will ensure user's '.uip', 
                # 'setup.py', and 'setup.cfg' will overwrite the default ones.
                template.copy_template(template_path, dir)

                for file_to_template in files_to_template:
                    if not os.path.exists(os.path.join(template_path, file_to_template)):
                        continue
                    rendered_template = formatting.jinja_render_file(
                        template_path, file_to_template, variable_dict,
                        **{'keep_trailing_newline': True, 'lstrip_blocks': True,
                        'trim_blocks': True})
                    custom_io.write_to_file(os.path.join(dir, file_to_template), rendered_template)

                # Generate UUIDs for all 'sysId' fields in template.json
                template_json_path = os.path.join(dir, constants.TEMPLATE_JSON_PATH)
                template_json = custom_io.read_json(template_json_path)
                if template_json is None:
                    raise customexceptions.FileNotFoundError(313, template_json_path)
                generic.update_key(template_json, constants.TEMPLATE_JSON_UUID_KEY,
                    generic.generate_uuid)
                custom_io.write_to_file(template_json_path, json.dumps(template_json, indent=2))

                # Save the 'template' for future use if the user specified
                if save and is_user_template:
                    save_user_specified_template(template_path, template_details)

                return 'Successfully initialized "%s (%s)" template in "%s"' % (
                    template_name, template_details['version'], dir)
        finally:
            if temp_folder:
                custom_io.remove_dir(temp_folder)


def get_built_extension_zip_path():
    dir = os.getcwd()
    if is_valid_dot_uip_and_extension_template_dir(dir):
        search_dir = os.path.join(dir, constants.EXTENSION_BUILD_DIR)
        zip_files = custom_io.get_files_of_specific_type(search_dir, '*.zip')

        if zip_files is None or len(zip_files) == 0:
            raise customexceptions.InvalidFolderError(310, search_dir)

        if len(zip_files) > 1:
            choice = custom_io.read_user_choice('Multiple zip files were found. Please select the one you wish to upload: ',
                                         zip_files)
            return choice
        elif len(zip_files) == 1:
            return zip_files[0]
    else:
        raise customexceptions.InvalidFolderError(309, dir)


def get_built_full_package_zip_path():
    dir = os.getcwd()
    if is_valid_dot_uip_and_extension_template_dir(dir):
        search_dir = os.path.join(dir, constants.PACKAGE_BUILD_DIR)
        zip_files = custom_io.get_files_of_specific_type(search_dir, '*.zip')

        if zip_files is None or len(zip_files) == 0:
            raise customexceptions.InvalidFolderError(310, search_dir)

        if len(zip_files) > 1:
            choice = custom_io.read_user_choice('Multiple zip files were found. Please select the one you wish to upload: ',
                                         zip_files)
            return choice
        elif len(zip_files) == 1:
            return zip_files[0]
    else:
        raise customexceptions.InvalidFolderError(309, dir)


def get_temporary_save_dir():
    dir = os.getcwd()
    if is_valid_dot_uip_and_extension_template_dir(dir):
        return os.path.join(dir, constants.DOT_UIP_FOLDER_NAME, constants.TEMP_SAVE_DIR_NAME)
    else:
        raise customexceptions.InvalidFolderError(309, dir)


def get_pull_command_save_dir():
    return get_temporary_save_dir()


def get_download_command_save_dir():
    dir = os.getcwd()
    if is_valid_dot_uip_and_extension_template_dir(dir):
        return os.path.join(dir, constants.PACKAGE_DOWNLOAD_DIR)
    else:
        raise customexceptions.InvalidFolderError(309, dir)


def move_template_json_icon(move_from):
    if os.path.exists(move_from):
        dot_uip_dir = os.getcwd()
        if is_valid_dot_uip_and_extension_template_dir(dot_uip_dir):
            new_template_json = os.path.join(move_from, 'template.json')
            new_template_icon = os.path.join(move_from, 'template_icon.png')

            move_to = os.path.join(dot_uip_dir, 'src', 'templates')
            curr_template_json = os.path.join(move_to, 'template.json')
            curr_template_icon = os.path.join(move_to, 'template_icon.png')

            changes = {
                'updated_files': [],
                'new_files': [],
                'unchanged_files': []
            }

            for curr_file, new_file in [(curr_template_json, new_template_json),
                                        (curr_template_icon, new_template_icon)]:
                curr_file_md5 = custom_io.get_md5_of_file(curr_file)
                new_file_md5 = custom_io.get_md5_of_file(new_file)

                if curr_file_md5 is None:
                    if new_file_md5:
                        # current file does not exist but new file does
                        changes['new_files'].append(formatting.get_filename_from_path(new_file))
                        custom_io.copy_file(new_file, move_to)
                else:
                    if new_file_md5:
                        if curr_file_md5 == new_file_md5:
                            # current and new file exists, and they are the same
                            changes['unchanged_files'].append(formatting.get_filename_from_path(curr_file))
                        else:
                            # new file differs from current file
                            changes['updated_files'].append(formatting.get_filename_from_path(curr_file))
                            custom_io.copy_file(new_file, move_to)

            custom_io.remove_dir(move_from)
            return changes
        else:
            raise customexceptions.InvalidFolderError(309, dot_uip_dir)


def move_full_package(full_package_path):
    if os.path.exists(full_package_path):
        dot_uip_dir = os.getcwd()
        if is_valid_dot_uip_and_extension_template_dir(dot_uip_dir):
            new_full_package = full_package_path

            move_to = get_download_command_save_dir()

            custom_io.make_dir(move_to)

            existing_zip_files = custom_io.get_files_of_specific_type(move_to, '*.zip')
            curr_full_package = None
            new_full_package_name = formatting.get_filename_from_path(new_full_package)
            for existing_zip_file in existing_zip_files:
                if new_full_package_name == formatting.get_filename_from_path(existing_zip_file):
                    curr_full_package = existing_zip_file
                    break

            changes = {
                'updated_file': '',
                'new_file': '',
                'unchanged_file': ''
            }

            for curr_file, new_file in [(curr_full_package, new_full_package)]:
                curr_file_md5 = custom_io.get_md5_of_zipfile(curr_file)
                new_file_md5 = custom_io.get_md5_of_zipfile(new_file)

                if curr_file_md5 is None:
                    if new_file_md5:
                        # current file does not exist but new file does
                        custom_io.copy_file(new_file, move_to)
                        copied_file_path = custom_io.get_most_recent_file(move_to, '*.zip')
                        changes['new_file'] = formatting.get_relative_path(copied_file_path)
                else:
                    if new_file_md5:
                        if curr_file_md5 == new_file_md5:
                            # current and new file exists, and they are the same
                            changes['unchanged_file'] = formatting.get_relative_path(curr_file)
                        else:
                            # new file differs from current file
                            changes['updated_file'] = formatting.get_relative_path(curr_file)
                            custom_io.copy_file(new_file, move_to)

            custom_io.remove_dir(formatting.get_dir_name(full_package_path))
            return changes
        else:
            raise customexceptions.InvalidFolderError(309, dot_uip_dir)


def get_template_json_property(property):
    dir = os.getcwd()
    if is_valid_dot_uip_and_extension_template_dir(dir):
        template_json_path = os.path.join(dir, 'src', 'templates', 'template.json')
        try:
            template_json = custom_io.read_json(template_json_path)
            return template_json.get(property, None)
        except ValueError as e:
            raise customexceptions.CorruptedFileError(306, str(e))
    else:
        return None


def get_template_name_from_template_json():
    template_name = get_template_json_property('name')
    if template_name:
        return template_name
    else:
        raise customexceptions.CorruptedFileError(312)


def is_setup_py_script_compatible():
    dot_uip_dir = os.getcwd()

    # Make sure the setup.py in the extension template is compatible.
    # If not, we will error out for now. Ideally, we should offer some
    # way for user to "upgrade" their extension environment using a
    # 'uip upgrade' command
    is_compatible = True

    setup_py_version = template.get_setup_py_script_version(
        os.path.join(dot_uip_dir, constants.SETUP_PY))

    if setup_py_version is None:
        # Must be an older setup.py or a newer one without version
        # information (which should never be the case)
        is_compatible = False
    else:
        if setup_py_version.major <= 1 and setup_py_version.minor < 4:
            # incompatible version
            is_compatible = False

    return is_compatible


def build_extension(build_dir='extension_build', zip_filename='',
                    dep_whl_only=False):
    dot_uip_dir = os.getcwd()
    if is_valid_dot_uip_and_extension_template_dir(dot_uip_dir):
        if not is_setup_py_script_compatible():
            # Raise an exception letting the user know the setup.py script is
            # outdated and needs to be upgraded using 'uip upgrade'
            raise customexceptions.CorruptedFileError(325)

        extension_yml = custom_io.read_yaml(os.path.join(dot_uip_dir,
                                            constants.EXTENSION_YML_PATH))

        error = formatting.validate_using_jsonschema(
                                extension_yml,
                                constants.VALID_EXTENSION_YML_SCHEMA)
        if error:
            raise customexceptions.CorruptedFileError(314,
                                        constants.EXTENSION_YML_PATH, error)

        if not formatting.validate_regex_input(
            constants.SEMVER_REGEX,
            extension_yml['extension']['version']
        ):
            raise customexceptions.InvalidValueError(321)

        # Assume extension is zip_safe, if 'zip_safe' is not in extension.yml
        zip_safe = extension_yml['extension'].get('zip_safe', True)

        # Make sure the 'dep_whl_only' flag is specified only if 'zip_safe' is False
        if dep_whl_only and zip_safe:
            raise customexceptions.InvalidValueError(324)

        dep_wheel_temp_dir = custom_io.get_temp_dir()
        extension_zip_temp_dir = custom_io.get_temp_dir()

        dep_wheel_path = None
        extension_zip_path = None
        try:
            # Install any third-party dependencies
            sandbox.run_setup(constants.SETUP_PY,
                              ['clean', '--all', 'install_deps'])
            if zip_safe == False:
                # Create the dependency wheel file in a temporary directory
                # so we can be sure whether it actually got generated or not.
                sandbox.run_setup(constants.SETUP_PY, ['clean', '--all',
                                'bdist_dep_whl', '--dist-dir', dep_wheel_temp_dir])
                temp_dep_wheel = custom_io.get_most_recent_file(
                                        dep_wheel_temp_dir, filetype='*.whl')
                if temp_dep_wheel is not None:
                    # Copy dependency wheel to the appropriate folder
                    dep_wheel_path = os.path.join(dot_uip_dir, 'dist', 'dep',
                                                os.path.basename(temp_dep_wheel))
                    custom_io.make_dir(os.path.dirname(dep_wheel_path))
                    custom_io.remove_file(dep_wheel_path)
                    custom_io.copy_file(temp_dep_wheel, dep_wheel_path)
            if not dep_whl_only:
                sandbox.run_setup(constants.SETUP_PY, ['clean', '--all',
                            'bdist_egg', '--dist-dir', extension_zip_temp_dir])

            print(('=' * 88))

            temp_extension_zip = custom_io.get_most_recent_file(
                                    extension_zip_temp_dir, filetype='*.zip')

            if dep_whl_only:
                return [dep_wheel_path]

            if temp_extension_zip:
                # Copy extension zip to the appropriate folder
                extension_zip_build_dir = os.path.join(dot_uip_dir, 'dist', build_dir)
                custom_io.make_dir(extension_zip_build_dir)
                if len(zip_filename) == 0:
                    zip_filename = os.path.basename(temp_extension_zip)
                extension_zip_path = os.path.join(extension_zip_build_dir, zip_filename)
                custom_io.remove_file(extension_zip_path)
                custom_io.copy_file(temp_extension_zip, extension_zip_path)

                if dep_wheel_path:
                    return [extension_zip_path, dep_wheel_path]
                else:
                    return [extension_zip_path]
            else:
                raise customexceptions.BuildError(304)
        except SystemExit:
            pass
        except ValueError as ve:
            # Expected if 'zip_safe' is specified for API level < 1.4.0 or
            # if the user provided non-pep compliant extension version
            raise customexceptions.InvalidValueError(602, str(ve))
        finally:
            custom_io.remove_dir(dep_wheel_temp_dir)
            custom_io.remove_dir(extension_zip_temp_dir)
    else:
        raise customexceptions.InvalidFolderError(309, dot_uip_dir)


def build_full_package():
    dot_uip_dir = os.getcwd()
    if is_valid_dot_uip_and_extension_template_dir(dot_uip_dir):
        full_package_build_dir = os.path.join(dot_uip_dir, 'dist', 'package_build')
        build_artifacts = build_extension(build_dir=full_package_build_dir,
                                        zip_filename='extension_archive.zip')
        # With the introduction of the new dependency wheel file, build_extension
        # can return a list. In such case, filter out everything but 'extension_archive.zip'
        build_artifacts = list(filter(lambda ezp: 'extension_archive.zip' in ezp,
                                            build_artifacts))
        if len(build_artifacts) != 1:
            raise customexceptions.BuildError(305)
        extension_zip_path = build_artifacts[0]

        template_json_path = os.path.join(dot_uip_dir, 'src', 'templates', 'template.json')
        template_json_data = custom_io.read_json(template_json_path)
        
        template_name = template_json_data.get('name', '').strip()
        if len(template_name) == 0:
            raise customexceptions.CorruptedFileError(306, "'name' must be defined.")

        template_name = re.sub(constants.UNIVERSAL_TEMPLATE_NAME_REGEX, '_', template_name.lower(), re.UNICODE)

        template_icon_path = os.path.join(dot_uip_dir, 'src', 'templates', 'template_icon.png')

        extension_yml_path = os.path.join(dot_uip_dir, 'src', 'extension.yml')
        extension_yml_data = custom_io.read_yaml(extension_yml_path)
        extension_version = extension_yml_data['extension']['version']
        if not formatting.validate_regex_input(constants.SEMVER_REGEX, extension_version):
            raise customexceptions.InvalidValueError(321)

        template_dist_name = constants.UNIVERSAL_TEMPLATE_DIST_NAME % (
            template_name,
            extension_version
        )

        template_dist_zip = os.path.join(full_package_build_dir, template_dist_name)
        with zipfile.ZipFile(template_dist_zip, 'w') as zf:
            zf.write(template_json_path, arcname=os.path.basename(template_json_path))

            if os.path.exists(template_icon_path):
                zf.write(template_icon_path, arcname=os.path.basename(template_icon_path))

            zf.write(extension_zip_path, arcname=os.path.basename(extension_zip_path))

        # delete extension_archive.zip
        custom_io.remove_file(extension_zip_path)

        most_recent_file = custom_io.get_most_recent_file(full_package_build_dir, '*.zip')
        if os.path.basename(most_recent_file) != template_dist_name:
            raise customexceptions.BuildError(305)
        else:
            return [template_dist_zip]
    else:
        raise customexceptions.InvalidFolderError(309, dot_uip_dir)


def generate_build(build_all=False, dep_whl_only=False):
    if build_all:
        return build_full_package()
    else:
        return build_extension(dep_whl_only=dep_whl_only)


def purge_build_artifacts(clean_all=False):
    dot_uip_dir = os.getcwd()
    if is_valid_dot_uip_and_extension_template_dir(dot_uip_dir):
        purged_files = []

        for build_artifact_dir in constants.BUILD_ARTIFACT_DIRS:
            build_artifact_dir = os.path.join(dot_uip_dir, build_artifact_dir)
            if os.path.exists(build_artifact_dir):
                purged_files.extend(custom_io.get_dir_listing(build_artifact_dir))
                purged_files.append(build_artifact_dir)
                custom_io.remove_dir(build_artifact_dir)

        if clean_all and os.path.exists(constants.THREEPP_DIR):
            # Purge the '3pp' folder, if it exists
            purged_files.append(constants.THREEPP_DIR)
            custom_io.remove_dir(constants.THREEPP_DIR)

        purged_files = [os.path.relpath(purged_file) for purged_file in purged_files]

        return purged_files
    else:
        raise customexceptions.InvalidFolderError(309, dot_uip_dir)


def get_dot_uip_config_file_path(relative_to=os.getcwd()):
    config_file_path = os.path.join(relative_to, constants.DOT_UIP_FOLDER_NAME, constants.CONFIG_FILE_DIR_NAME,
                                    constants.CONFIG_FILE_NAME)
    return config_file_path if os.path.exists(config_file_path) else None


def upgrade_extension_repo(repo_dir):
    dot_uip_dir = repo_dir

    if not is_valid_dot_uip_and_extension_template_dir(dot_uip_dir,
                                                   require_setup_files=False):
        raise customexceptions.InvalidFolderError(309, dot_uip_dir)

    # For now, the upgrade process involves replacing the setup.py and 
    # setup.cfg scripts with the newer versions and making a backup of the
    # original ones. If they do not exist, then they will be added.

    backup_folder = os.path.join(dot_uip_dir, constants.BACKUP_FOLDER_NAME)

    setup_cfg_path = os.path.join(dot_uip_dir, constants.SETUP_CFG)
    setup_py_path = os.path.join(dot_uip_dir, constants.SETUP_PY)

    scripts_backed_up = []

    if os.path.exists(setup_cfg_path):
        custom_io.make_dir(backup_folder)
        custom_io.copy_file(setup_cfg_path, os.path.join(backup_folder,
                                        constants.SETUP_CFG))
        scripts_backed_up.append(constants.SETUP_CFG)

    if os.path.exists(setup_py_path):
        custom_io.make_dir(backup_folder)
        custom_io.copy_file(setup_py_path, os.path.join(backup_folder,
                                        constants.SETUP_PY))
        scripts_backed_up.append(constants.SETUP_PY)

    template.copy_setup_scripts(dot_uip_dir)

    msg = '{0} and {1} have been '.format(constants.SETUP_CFG,
                                                    constants.SETUP_PY)
    if len(scripts_backed_up) > 0:
        msg += 'upgraded (original files were backed up in {} folder)'.format(
            os.path.relpath(backup_folder)
        )
    else:
        msg += 'added'

    return msg