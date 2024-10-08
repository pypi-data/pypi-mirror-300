import os
import argparse

# cliapis
UNIVERSAL_TEMPLATE_URL_ENDPOINT = 'resources/universaltemplate'
TASK_URL_ENDPOINT = 'resources/task'
TASK_INSTANCE_URL_ENDPOINT = 'resources/taskinstance'

# cliconfig
ADJUSTED_WRAP_LIMIT = '82'

# uipproject
CONFIG_FILE_NAME = 'uip.yml'
CONFIG_FILE_DIR_NAME = 'config'
DOT_UIP_FOLDER_NAME = '.uip'
SETUP_CFG = 'setup.cfg'
SETUP_PY = 'setup.py'
SETUP_SCRIPTS_PATH = 'setupscripts'
BACKUP_FOLDER_NAME = '.backup'
EXTENSION_PY_PATH = 'src/extension.py'
EXTENSION_YML_PATH = 'src/extension.yml'
TEMPLATE_JSON_PATH = 'src/templates/template.json'
VALID_EXTENSION_TEMPLATE_FILES = [EXTENSION_PY_PATH, EXTENSION_YML_PATH, TEMPLATE_JSON_PATH, SETUP_PY,
                                  SETUP_CFG]
VALID_EXTENSION_TEMPLATE_FILES_WITHOUT_SETUP = [EXTENSION_PY_PATH, EXTENSION_YML_PATH, TEMPLATE_JSON_PATH]
SETUP_CFG_RESOURCE_PATH = '{0}/{1}'.format(SETUP_SCRIPTS_PATH, SETUP_CFG)
SETUP_PY_RESOURCE_PATH = '{0}/{1}'.format(SETUP_SCRIPTS_PATH, SETUP_PY)
SETUP_SCRIPTS_RESOURCES = [SETUP_CFG_RESOURCE_PATH, SETUP_PY_RESOURCE_PATH]
VARIABLES_OPTION_VALUE_DELIMETER = '='
VARIABLES_FILE_PREFIX = '@'
VARIABLES_JSON_STRING_PREFIX = '{'
VARIABLES_JSON_STRING_SUFFIX = '}'
DIST_DIR_NAME = 'dist'
EXTENSION_BUILD_DIR = os.path.join(DIST_DIR_NAME, 'extension_build')
PACKAGE_BUILD_DIR = os.path.join(DIST_DIR_NAME, 'package_build')
PACKAGE_DOWNLOAD_DIR = os.path.join(DIST_DIR_NAME, 'package_download')
TEMP_SAVE_DIR_NAME = 'tmp'
UNIVERSAL_TEMPLATE_DIST_NAME = 'unv_tmplt_%s-%s.zip'
THREEPP_DIR = '3pp'
BUILD_ARTIFACT_DIRS = ['build', 'dist', 'temp']
SEMVER_REGEX = r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
UNIVERSAL_TEMPLATE_NAME_REGEX = r"[^\w.]+"
VALID_EXTENSION_YML_SCHEMA = {
    "type": "object",
    "properties": {
        "extension": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string"
                },
                "version": {
                    "type": "string"
                },
                "api_level": {
                    "type": "string"
                },
                "requires_python": {
                    "type": "string"
                },
                "python_extra_paths": {
                    "type": "string"
                },
                "zip_safe": {
                    "type": "boolean"
                }
            },
            "required": ["name", "version", "api_level"]
        },
        "owner": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string"
                },
                "organization": {
                    "type": "string"
                }
            }
        },
        "comments": {
            "type": "string"
        }
    },
    "required": ["extension"]
}

# uiptemplates
BUILT_IN_TEMPLATES = ['ue-task', 'ue-publisher']
TEMPLATE_FOLDERS = ['tasktemplates', 'eventtemplates', '_usertemplates_']
TEMPLATE_NAME_VERSION_SEPARATOR = '@'
UE_TASK_VERSION = '1.0.0'
UE_PUBLISHER_VERSION = '1.0.0'
TEMPLATE_CONFIG_YAML = 'template_config.yml'
RESOURCES_DIR = os.path.join('uiptemplates', 'resources')
TEMPLATE_JSON_UUID_KEY = 'sysId'
VALID_USER_EXTENSION_TEMPLATE_FILES = {f for f in [EXTENSION_PY_PATH, EXTENSION_YML_PATH, TEMPLATE_JSON_PATH, 'template_config.yml']}
VALID_TEMPLATE_CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
        },
        "version": {
            "type": "string"
        },
        "description": {
            "type": "string",
        },
        "files_to_template": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "variables": {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "properties": {
                    "default": {
                        "type": ["number", "string", "integer", "object",
                                 "array", "boolean", "null"]
                    },
                    "description": {
                        "type": "string"
                    }
                },
                "required": ["default", "description"]
            }
        }
    },
    "required": ["name", "version", "description"],
    "dependentRequired": {
        "variables": ["files_to_template"],
        "files_to_template": ["variables"]
    }
}
TEMP_DIRECTORY_PREFIX = 'uip_cli_'
USER_TEMPLATES_PATH = os.path.join('uiptemplates', '_usertemplates_')
#
# (branch|commit|tag) captures the 1st group which will contain one of
# "branch", "commit", or "tag".
#
# (.+) captures the 2nd group which will be the value of branch/commit/tag
#
#
GIT_BRANCH_COMMIT_TAG_REGEX = r"(?:@(branch|commit|tag):(.+))$"
ZIP_CONTENT_TYPES = [
    'application/octet-stream',
    'multipart/x-zip',
    'application/zip',
    'application/zip-compressed',
    'application/x-zip-compressed',
    'application/x-zip'
]


# parsecli
_TASK_STATUSES = {
    'success': 'Success',
    'finished': 'Finished',
    'failed': 'Failed',
    'cancelled': 'Cancelled',
    'start_failure': 'Start Failure',
    'undeliverable': 'Undeliverable',
    'in_doubt': 'In Doubt',
    'skipped': 'Skipped'
}
TASK_STATUSES = argparse.Namespace(**_TASK_STATUSES)


# EXIT CODES
SUCCESS = 0
ERROR = 1
