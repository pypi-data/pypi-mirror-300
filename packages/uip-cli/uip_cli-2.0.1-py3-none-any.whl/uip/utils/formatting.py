import json
import os
import re
import jsonschema
from jinja2 import Environment, FileSystemLoader
from collections import namedtuple
import textwrap

import prettytable
from uip.exceptions import customexceptions


def print_table(table_headers, table_data, max_width=120, separate_each_entry=False,
    as_json=False):
    table = prettytable.PrettyTable(table_headers)
    for data in table_data:
        table.add_row(data)
    table.max_width = max_width
    table.align = "l"
    if separate_each_entry:
        table.hrules = prettytable.ALL
    print(table.get_json_string() if as_json else table)


def parse_json_string(json_string):
    try:
        return json.loads(json_string)
    except ValueError as ve:
        raise customexceptions.InvalidValueError(401, json_string)


def wrap_text(text, width=80, initial_indent=0, subsequent_indent=0):
    """
    Wraps text after a specified width limit, and adjusts
    indentation based on specified indent parameters

    Parameters
    ----------
    text : str
        The text to wrap
    width : int, optional
        The max number of characters in a line, by default 80
    initial_indent : int, optional
        How much to indent the first line by, by default 0
    subsequent_indent : int, optional
        How much to indent the remaining lines by, by default 0

    Returns
    -------
    str
        The wrapped text
    """
    lines = textwrap.dedent(text).strip().splitlines()

    wrapped_lines = [textwrap.fill(line, width=width, initial_indent=' ' * initial_indent,
                                   subsequent_indent=' ' * subsequent_indent) for line in lines]
    return '\n'.join(wrapped_lines)


def format_error_style(error):
    if isinstance(error, Exception):
        error_type = error.__class__.__name__
        error_msg = str(error.message) if hasattr(
            error, 'message') and error.message else str(error)
        return '[%s] %s' % (error_type, error_msg)
    else:
        return 'Unknown error occurred'


def get_filename_from_path(filepath):
    return os.path.basename(filepath)


def get_relative_path(filepath):
    if filepath:
        return os.path.relpath(filepath)
    else:
        return None


def get_dir_name(filepath):
    if filepath:
        return os.path.dirname(filepath)
    else:
        return None


def format_list_for_printing(list, header=''):
    formatted_list_output = '%s:\n' % header if header else ''
    formatted_list = ['  - %s\n' % element for element in list]
    for formatted_element in formatted_list:
        formatted_list_output += formatted_element

    return formatted_list_output


def jinja_render_file(folder_containing_file, filename, variables, **kwargs):
    def custom_error_filter(msg):
        raise customexceptions.InvalidValueError(323, filename, msg)

    env = Environment(loader=FileSystemLoader(folder_containing_file),
                      **kwargs)
    env.filters['raise_error'] = custom_error_filter
    curr_template = env.get_template(filename)
    return curr_template.render(variables)


def join_list_of_strings(input_list, conjunction='and'):
    conjunction = ' %s ' % conjunction.strip()

    if len(input_list) == 1:
        return input_list[0]
    elif len(input_list) == 2:
        return conjunction.join(input_list)
    else:
        return ', '.join(input_list[:-1]) + (',%s' % conjunction) + input_list[-1]


def replace_nonalphanum_chars(input_str, replace_with='_'):
    return re.sub(r'[^\w]+', replace_with, input_str, re.UNICODE)


def validate_regex_input(expression, input_string):
    return re.search(expression, input_string) != None


def validate_using_jsonschema(dict_obj, schema):
    """Returns an empty string, if the 'dict_obj' conforms
    to 'schema'

    Parameters
    ----------
    dict_obj : dict
        dictionary object to verify
    schema : dict
        schema used to verify 'dict_obj' with

    Returns
    -------
    str
        an empty string, if valid else the error message
    """
    try:
        jsonschema.validate(dict_obj, schema)
        return ''
    except Exception as e:
        return str(e)


class VersionInfo(namedtuple("VersionInfo", "major minor patch")):
    def __new__(cls, version):
        return super().__new__(cls, *map(int, version.split(".")))

    def __repr__(self):
        return ".".join(map(str, self))