# cliapis errors (1-100)
cliapis_errors = {
    1: 'auth tuple cannot be None',
    2: 'params dictionary cannot be None',
    3: 'response object cannot be None',
    4: 'Universal Template name must be specified',
    5: 'url cannot be empty',
    6: '"{0}" command type not found',
    7: 'url endpoint for "%s" not found',
    8: '"{0}" not found',
    9: 'There are no existing instances of "{0}" task'
}

# cliconfig errors (101-200)
cliconfig_errors = {
    101: '"{0}" is not a JSON file',
    102: '"{0}" is not a PNG file',
    103: '"{0}" is not a ZIP file'
}

# config errors (201-300)
config_errors = {
    201: '"{0}" must be specified',
    202: 'Universal Template name must be specified',
    203: '"{0}" option cannot be None',
    204: '"{0}" configuration file not found',
    205: 'Universal Extension task name must be specified',
    206: '"{0}" is not a valid integer value',
    207: 'value must be a positive integer',
    208: '"{0}" is not a supported platform. Only Windows, Linux, and MacOS are supported',
    209: 'value cannot be empty'
}

# uipproject errors (301-400)
uipproject_errors = {
    301: '"{0}" is not a valid JSON or YAML file',
    302: '"{0}" is incorrectly formatted',
    303: '{0} folder already exists in "{1}"',
    304: 'error building extension',
    305: 'error building full package',
    306: 'template.json is corrupted. {0}',
    307: '"{0}" already contains an Extension template',
    308: '"{0}" does not contain a valid Extension template',
    309: '"{0}" is not a valid Extension template directory',
    310: 'No zip files were found in "{0}"',
    311: '"{0}" is not a valid Extension template',
    312: 'template.json is corrupted. The "name" field must be non-empty',
    313: '"{0}" not found',
    314: '"{0}" is invalid. {1}',
    315: 'template name must be something other than {0}',
    316: 'multiple matching templates found. Specify one of the following versions: {0}.',
    317: 'template must be specified.',
    318: 'Unable to clone the specified Git repository. Ensure the URL is valid.',
    319: 'HTTP(S) request failed with code {0}: {1}.',
    320: 'URL must point to a valid zip file.',
    321: 'extension version must be SemVer compliant',
    322: 'Unable to add "{0}"',
    323: '"{0}" contains invalid jinja2 syntax: {1}',
    324: 'Dependency wheel cannot be built if zip_safe is True',
    325: 'setup.py is incompatible with this version of uip-cli. Run "uip init --upgrade"'
}

# utils errors (401-500)
utils_errors = {
    401: '"{0}" is not a valid JSON string'
}

# parsecli errors (501-600)
parsecli_errors = {
    501: '"{0}" is not a valid folder name',
    502: '"{0}" is not a valid Extension template',
    503: '"{0}" is not a valid Universal Extension task',
    504: '"{0}" is not a valid task instance number'
}

# Generic errors (601-700)
generic_errors = {
    601: 'Unable to create "{0}"',
    602: '{0}',  # Can be used if error is coming from an external source
    603: '{0} not found',
    604: '{0} expected to be one of {1}',
    605: '"{0}" is not valid'
}

error_messages = {}
error_messages.update(cliapis_errors)
error_messages.update(cliconfig_errors)
error_messages.update(config_errors)
error_messages.update(uipproject_errors)
error_messages.update(utils_errors)
error_messages.update(parsecli_errors)
error_messages.update(generic_errors)