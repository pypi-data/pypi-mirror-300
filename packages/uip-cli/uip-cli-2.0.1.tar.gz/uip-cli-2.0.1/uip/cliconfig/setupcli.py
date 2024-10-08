import argparse
import os
import sys

from uip.cliconfig.customformatter import CustomHelpFormatter
from uip.config.configoptions import get_default_value as gdv
from uip.config.configoptions import get_env_var_name as gevn
from uip.config.configoptions import get_long_arg as gla
from uip.config.configoptions import get_short_arg as gsa
from uip.constants import constants
from uip.parsecli.parsecli import parse_cli_args
from uip.utils.formatting import wrap_text, join_list_of_strings
from .. import UIP_CLI_VERSION

prog_ref = "%(prog)s"

def add_example_epilog(cmd_arg, example_usage, title="examples"):
    """
    Adds examples section at the end of the help menu

    Parameters
    ----------
    cmd_arg : parser, subparser
        The parser or subparser to add the examples to
    example_usage : str
        The examples to add
    """
    # At this point, example_usage contains %(prog)s instead of the actual program name (which is substituted later).
    # Thus, effective_width needs to account for this as shown below.
    effective_width = 80 - (len(cmd_arg.prog) - len(prog_ref))
    wrapped_usage = wrap_text(example_usage, effective_width, initial_indent=2, subsequent_indent=4)
    title = wrap_text(title, effective_width, initial_indent=0, subsequent_indent=2)
    wrapped_usage = '\n%s: \n%s\n' % (title, wrapped_usage)
    cmd_arg.formatter_class = CustomHelpFormatter
    if cmd_arg.epilog:
        cmd_arg.epilog += wrapped_usage
    else:
        cmd_arg.epilog = wrapped_usage


def add_command_description(cmd_arg, description, title="description"):
    effective_width = 80
    wrapped_description = wrap_text(description, effective_width, initial_indent=2, subsequent_indent=2)
    title = wrap_text(title, effective_width, initial_indent=0, subsequent_indent=2)
    wrapped_description = '\n%s: \n%s\n' % (title, wrapped_description)
    cmd_arg.formatter_class = CustomHelpFormatter
    if cmd_arg.description:
        cmd_arg.description += wrapped_description
    else:
        cmd_arg.description = wrapped_description


validation_funcs = []


def add_login_args(cmd_arg):
    """
    Adds login related arguments to cmd_arg

    Parameters
    ----------
    cmd_arg : parser, subparser
        The parser or subparser to add the login args to
    """
    login_group = cmd_arg.add_argument_group('login required arguments')

    login_group.add_argument(gsa('shared.userid'), gla('shared.userid'), metavar='<userid>',
                             type=str,
                             help='username used to log into Controller Web Services API (environment variable: %s)'
                                  % gevn('shared.userid'))
    login_group.add_argument(gsa('shared.password'), gla('shared.password'), metavar='<password>', type=str,
                             help='password used to log into Controller Web Services API (environment variable: %s)'
                                  % gevn('shared.password'))
    login_group.add_argument(gsa('shared.url'), gla('shared.url'), metavar='<url>', type=str,
                             help='url used to connect to the Controller (environment variable: %s)' % gevn(
                                 'shared.url'))


def setup_init_arg(cmd_subparsers):
    """
    Sets up the init command and it's arguments

    Parameters
    ----------
    cmd_subparsers : subparsers
        The subparser to add the init arg to
    """
    init_arg = cmd_subparsers.add_parser('init', help='initialize a new project with starter Extension templates')
    add_command_description(init_arg,
                            "The 'init' command provides starter Extension templates to start a new project")

    # Add positional arguments
    init_arg.add_argument('dir', metavar='<dir>', default=gdv('init.dir'), nargs='?', type=str,
                          help='where to initialize the Extension template (default: %(default)s)')


    extension_template_arg_ref = 'init.extension_template'
    variables_arg_ref = 'init.variables'
    save_arg_ref = 'init.save'
    upgrade_arg_ref = 'init.upgrade'

    # Add optional arguments
    init_arg.add_argument(gsa(extension_template_arg_ref), gla(extension_template_arg_ref), metavar='<name>',
                          default=gdv(extension_template_arg_ref), type=str,
                          help='name of the Extension template to initialize in the specified directory. '
                               'If there are multiple templates with the same name, the version must also '
                               'be specified as <template>@<version>. If no name is specified, an empty '
                               '.uip project will be created.')
    init_arg.add_argument(gsa(variables_arg_ref), gla(variables_arg_ref), metavar='<variables>',
                          default=gdv(variables_arg_ref), action='append',
                          help='user defined variables used to configure templates before creating them. '
                               '(environment variable: %s)' % gevn(variables_arg_ref))
    init_arg.add_argument(gsa(save_arg_ref), gla(save_arg_ref), default=None,
                           action='store_true', help='if specified, the user specified template will be saved for future use. ')
    init_arg.add_argument(gsa(upgrade_arg_ref), gla(upgrade_arg_ref), default=None,
                           action='store_true',
                           help="if specified, the existing Extension project will be "
                                "upgraded to meet the CLI's new requirements. "
                                "For now, this involves upgrading the setup scripts "
                                "(script.py and setup.cfg).")
    
    def validate_init_args(parser, args):
        if args and args.command_type == 'init':
            if args.upgrade and (args.extension_template is not None or \
                                 args.variables is not None or \
                                 args.save is not None):
                parser.error('The {0} option cannot be specified with {1}'.
                             format(gla(upgrade_arg_ref), join_list_of_strings([
                                gla(extension_template_arg_ref),
                                gla(variables_arg_ref),
                                gla(save_arg_ref)], 'or')))

    validation_funcs.append(validate_init_args)

    # Add examples
    add_example_epilog(init_arg, """
        {prog}
        {prog} {ula}
        {prog} {ietsa} <template name>@<template version>
        {prog} {ietsa} <template name> {itvsa} '{{"extension_name": "myext", "version": "1.0.0"}}'
        {prog} {ietsa} <template name> {itvsa} 'extension_name=myext' {itvsa} 'version=1.0.0'
        {prog} {ietsa} <template name> {itvsa} @vars.json
        {prog} {ietsa} <template name> {itvsa} @vars.yml
        {prog} {ietsa} <template name>@<template version>
        {prog} {ietsa} <template zip> {itvsa} @vars.yml {itsla}
        {prog} {ietsa} <HTTP(S) link to zip> {itssa}
    """.format(prog=prog_ref, ietsa=gsa(extension_template_arg_ref), itvsa=gsa(variables_arg_ref),
        itssa=gsa(save_arg_ref), itsla=gla(save_arg_ref), ula=gla(upgrade_arg_ref)))


def setup_template_list_arg_deprecated(cmd_subparsers):
    """
    NOTE: This command will be deprecated in two releases. Currently, replace by
    'template' command.
    """
    template_list = cmd_subparsers.add_parser('template-list',
                                              help='list of available Extension templates. Note: this command will be deprecated in two releases')
    add_command_description(template_list, "List of available Extension templates. \nNote: this command will be deprecated in two releases. Use the 'template' command instead.")

    # Add positional arguments
    template_list.add_argument('extension_template', metavar="<extension template>", nargs='?', type=str,
                               default=None, help='Extension template to list variables of')

    # Add examples
    add_example_epilog(template_list, """
        %(prog)s
        %(prog)s <template name>
    """)


def setup_template_list_arg(template_subparser):
    template_list_arg = template_subparser.add_parser('list', help='list available Extension templates (and their variables)')
    add_command_description(template_list_arg, 
                            "used to list available Extension templates. If a template name isn't specified, the CLI will "
                            "print all the available templates. Specifying the template name will print the template's "
                            "variables.")

    # Add positional arguments
    template_list_arg.add_argument('extension_template', metavar="<extension template>", nargs='?', type=str,
                               default=None, help='Extension template to list variables of. If there are multiple '
                                                  'templates with the same name, the version must also be specified '
                                                  'as <template>@<version>')

    # Add optional arguments
    template_list_arg.add_argument(gsa('template_list.json'), gla('template_list.json'), default=None,
                           action='store_true', help='if specified, the output will be printed as a JSON string. ')

    # Add examples
    add_example_epilog(template_list_arg, """
        {prog}
        {prog} {tljla}
        {prog} <template name>
        {prog} <template name>@<template version>
        {prog} <template name> {tljla}
    """.format(prog=prog_ref, tljla=gla('template_list.json')))


def setup_template_add_arg(template_subparser):
    template_add_arg = template_subparser.add_parser('add', help='add an external Extension template')
    add_command_description(template_add_arg, 
                            "used to add external Extension templates. Valid values include path to a zip file, "
                            "HTTP(S) url pointing to a zip file, or a Git repository clone url. "
                            "See the full documentation for details.")

    # Add positional arguments
    template_add_arg.add_argument('extension_template', metavar="<extension template>", type=str,
                               default=None, help='Extension template to add')

    # Add examples
    add_example_epilog(template_add_arg, """
        %(prog)s <path to zip file>
        %(prog)s <HTTP(S) url to a zip file>
        %(prog)s <Git Repository Clone url>
    """)


def setup_template_delete_arg(template_subparser):
    template_delete_arg = template_subparser.add_parser('delete', help='delete an Extension template')
    add_command_description(template_delete_arg, 
                            "the specified Extension template will be deleted.")

    # Add positional arguments
    template_delete_arg.add_argument('extension_template', metavar="<extension template>", type=str,
                               default=None, help='Extension template to delete. If there are multiple '
                                                  'templates with the same name, the version must also be specified '
                                                  'as <template>@<version>')

    # Add examples
    add_example_epilog(template_delete_arg, """
        %(prog)s <template name>
        %(prog)s <template name>@<template version>
    """)


def setup_template_export_arg(template_subparser):
    template_export_arg = template_subparser.add_parser('export', help='export an Extension template')
    add_command_description(template_export_arg, 
                            "the specified Extension template will be exported.")

    # Add positional arguments
    template_export_arg.add_argument('extension_template', metavar="<extension template>", type=str,
                               default=None, help='Extension template to export. If there are multiple '
                                                  'templates with the same name, the version must also be specified '
                                                  'as <template>@<version>')

    # Add examples
    add_example_epilog(template_export_arg, """
        %(prog)s <template name>
        %(prog)s <template name>@<template version>
    """)


def setup_template_arg(cmd_subparsers):
    template_arg = cmd_subparsers.add_parser('template', help='used to perform actions on built-in (and external) templates')
    template_subparser = template_arg.add_subparsers(title="template action", dest='template_action', metavar='')
    template_subparser.required = True

    add_command_description(template_arg,
                            'used to perform actions on built-in (and external) templates.')

    setup_template_list_arg(template_subparser)
    setup_template_add_arg(template_subparser)
    setup_template_delete_arg(template_subparser)
    setup_template_export_arg(template_subparser)

    # Add examples
    add_example_epilog(template_arg, """
        %(prog)s list
        %(prog)s list <template name>
        %(prog)s add <template zip / HTTP(S) link to zip / Git Repo>
        %(prog)s delete <template name>
        %(prog)s delete <template name>@<template version>
        %(prog)s export <template name>
    """)


def setup_build_arg(cmd_subparsers):
    """
    Sets up the build command and it's arguments

    Parameters
    ----------
    cmd_subparsers : subparsers
        The subparser to add the build arg to
    """
    build_all_arg_ref = 'build.all'
    build_dep_whl_only_arg_ref = 'build.dep_whl_only'

    build_arg = cmd_subparsers.add_parser('build', help='used to build Extension or full package')
    add_command_description(build_arg,
                            "The 'build' command is used to build the Extension or the full package. By default, "
                            "only the Extension will be built.")

    # Add optional arguments
    mutually_exclusive_args = build_arg.add_mutually_exclusive_group()
    mutually_exclusive_args.add_argument(gsa(build_all_arg_ref), gla(build_all_arg_ref), default=None,
                           action='store_true', help='if specified, the full package will be built '
                                                     '(environment variable: %s)' % gevn(build_all_arg_ref))
    mutually_exclusive_args.add_argument(gsa(build_dep_whl_only_arg_ref), gla(build_dep_whl_only_arg_ref), default=None,
                           action='store_true', help='if specified, only the dependency wheel file will be built '
                                                     '(environment variable: %s)' % gevn(build_dep_whl_only_arg_ref))

    # Add examples
    add_example_epilog(build_arg, """
        {prog} 
        {prog} {basa}
        {prog} {bdwola}
    """.format(prog=prog_ref, basa=gsa(build_all_arg_ref),
               bdwola=gla(build_dep_whl_only_arg_ref)))


def setup_upload_arg(cmd_subparsers):
    upload_arg = cmd_subparsers.add_parser('upload', help='upload Extension (or full package) to the Controller')
    add_command_description(upload_arg, "upload Extension (or full package) to the Controller. By default, only the "
                                        "Extension will be uploaded.")

    # Add optional arguments
    upload_arg.add_argument(gsa('upload.all'), gla('upload.all'), default=None,
                            action='store_true', help='if specified, the full package will be uploaded '
                                                      '(environment variable: %s)' % gevn('upload.all'))
    # Add required arguments related to login
    add_login_args(upload_arg)

    # Add examples
    add_example_epilog(upload_arg, """
        {prog}
        {prog} {uala}
    """.format(prog=prog_ref, uala=gla('upload.all')))


def setup_push_arg(cmd_subparsers):
    push_arg = cmd_subparsers.add_parser('push', help='build and upload Extension (or full package) to the Controller')
    add_command_description(push_arg,
                            "build and upload Extension (or full package) to the Controller. By default, only the "
                            "Extension will be built and uploaded.")

    # Add optional arguments
    push_arg.add_argument(gsa('push.all'), gla('push.all'), default=None,
                          action='store_true', help='if specified, the full package will be built and uploaded '
                                                    '(environment variable: %s)' % gevn('push.all'))
    # Add required arguments related to login
    add_login_args(push_arg)

    # Add examples
    add_example_epilog(push_arg, """
        {prog}
        {prog} {pala}
    """.format(prog=prog_ref, pala=gla('push.all')))


def setup_pull_arg(cmd_subparsers):
    pull_arg = cmd_subparsers.add_parser('pull',
                                         help='pulls the latest template.json (and template_icon.png, if present)')
    add_command_description(pull_arg, "pulls the latest template.json (and template_icon.png, if present)")

    # Add required arguments related to login
    add_login_args(pull_arg)

    # Add examples
    add_example_epilog(pull_arg, """
        {prog}
        {prog} {sula} admin {spla} admin
    """.format(prog=prog_ref, sula=gla('shared.userid'), spla=gla('shared.password')))


def setup_download_arg(cmd_subparsers):
    download_arg = cmd_subparsers.add_parser('download', help='downloads the full Universal Template package')
    add_command_description(download_arg,
                            'downloads the full Universal Template package and saves the zip in the "dist" folder')

    # Add optional arguments
    download_arg.add_argument(gsa('download.template_name'), gla('download.template_name'), type=str,
                              metavar='<name>',
                              help='name used within the Controller to identify the Universal Template'
                                   ' (environment variable: %s)' % gevn('download.template_name'))

    # Add required arguments related to login
    add_login_args(download_arg)

    # Add examples
    add_example_epilog(download_arg, """
          {prog} {dtnsa} <template name>
          {prog} {susa} admin {spsa} admin
      """.format(prog=prog_ref, dtnsa=gsa('download.template_name'), susa=gsa('shared.userid'),
                 spsa=gsa('shared.password')))

def setup_clean_arg(cmd_subparsers):
    """
    Sets up the clean command and it's arguments

    Parameters
    ----------
    cmd_subparsers : subparsers
        The subparser to add the clean arg to
    """
    clean_all_arg_ref = 'clean.all'

    clean_arg = cmd_subparsers.add_parser('clean', help='used to purge build artifacts')
    add_command_description(clean_arg,
                            "The 'clean' command is used to purge build artifacts which "
                            "includes anything inside the dist, build, and temp folders.")
    
    # Add optional arguments
    clean_arg.add_argument(gsa(clean_all_arg_ref), gla(clean_all_arg_ref), default=None,
                          action='store_true', help='if specified, the 3pp folder will also be purged '
                                                    '(environment variable: %s)' % gevn(clean_all_arg_ref))

    # Add examples
    add_example_epilog(clean_arg, """
        {prog} 
        {prog} {cala}
    """.format(prog=prog_ref, cala=gla(clean_all_arg_ref)))

def setup_task_launch_arg(task_subparser):
    launch_task_arg = task_subparser.add_parser('launch', help='launch an Universal Extension task')
    add_command_description(launch_task_arg, 
                            'used to launch an Universal Extension task. By default, the CLI will '
                            'launch the task and continously print the status. Once the task '
                            'succeeds/fails, it will print the task output.')

    # Add positional arguments
    launch_task_arg.add_argument('task_name', metavar="<task name>", type=str, default=None, 
                        help='name of the Universal Extension task to launch')

    # Add optional arguments
    launch_task_arg.add_argument(gsa('task_launch.no_wait'), gla('task_launch.no_wait'), default=None,
                          action='store_true', help='if specified, the task will be launched, but task status and output will not be returned '
                                                    '(environment variable: %s)' % gevn('task_launch.no_wait'))


    # Add required arguments related to login
    add_login_args(launch_task_arg)

    # Add examples
    add_example_epilog(launch_task_arg, """
        %(prog)s <task name>
        %(prog)s <task name> {ltsa}
        %(prog)s <task name> {ltla}
    """.format(ltsa=gsa('task_launch.no_wait'), ltla=gla('task_launch.no_wait')))


def setup_task_status_arg(task_subparser):
    status_task_arg = task_subparser.add_parser('status', help='get status of an Universal Extension task instances')
    add_command_description(status_task_arg, 
                            'used to get the status and exit code of Universal Extension task instances')

    # Add positional arguments
    status_task_arg.add_argument('task_name', metavar="<task name>", type=str, default=None, 
                        help='name of the Universal Extension task to get status of')

    # Add optional arguments
    status_task_arg.add_argument(gsa('task_status.num_instances'), gla('task_status.num_instances'), metavar='<int>',
                          type=int,
                          help='number of task instances to get the status of (most recent first). If a '
                               'nonpositive number is provided, the status of all the instances will be shown. '
                               '(default value: %d, environment variable: %s)' 
                               % (gdv('task_status.num_instances'), gevn('task_status.num_instances')))

    # Add required arguments related to login
    add_login_args(status_task_arg)

    # Add examples
    add_example_epilog(status_task_arg, """
        %(prog)s <task name>
        %(prog)s <task name> {stsa} 5
        %(prog)s <task name> {stla} 0 
    """.format(stsa=gsa('task_status.num_instances'), stla=gla('task_status.num_instances')))


def setup_task_output_arg(task_subparser):
    output_task_arg = task_subparser.add_parser('output', help='get output of an Universal Extension task instance')
    add_command_description(output_task_arg, 
                            'used to get the output of an Universal Extension task instance')

    # Add positional arguments
    output_task_arg.add_argument('task_name', metavar="<task name>", type=str, default=None, 
                        help='name of the Universal Extension task to get the output of')

    # Add optional arguments
    output_task_arg.add_argument(gsa('task_output.instance_number'), gla('task_output.instance_number'), metavar='<int>',
                          type=int,
                          help='the instance number of the task instance to get the output of. By default, the output of '
                               'the most recent task instance will be returned. (environment variable: %s)' % gevn('task_output.instance_number'))

    # Add required arguments related to login
    add_login_args(output_task_arg)

    # Add examples
    add_example_epilog(output_task_arg, """
        %(prog)s <task name>
        %(prog)s <task name> {otsa} 134
        %(prog)s <task name> {otla} 34
    """.format(otsa=gsa('task_output.instance_number'), otla=gla('task_output.instance_number')))


def setup_task_arg(cmd_subparsers):
    task_arg = cmd_subparsers.add_parser('task', help='used to perform actions on Universal Extension tasks')
    task_subparser = task_arg.add_subparsers(title="task action", dest='task_action', metavar='<action>')
    task_subparser.required = True

    add_command_description(task_arg,
                            'used to perform actions on Universal Extension tasks')

    setup_task_launch_arg(task_subparser)
    setup_task_status_arg(task_subparser)
    setup_task_output_arg(task_subparser)

    # Add examples
    add_example_epilog(task_arg, """
        %(prog)s launch <task name>
        %(prog)s status <task name>
        %(prog)s output <task name>
    """)


def setup_cli_args(args_list=[]):
    """
    Sets up the cli arguments
    """
    # set help menu wrap limit to 82 characters which effectively results in 80 as argparse subtracts 2 internally
    os.environ['COLUMNS'] = constants.ADJUSTED_WRAP_LIMIT

    parser = argparse.ArgumentParser()

    add_example_epilog(parser, """
        %(prog)s <command>
        %(prog)s init
        %(prog)s download           
    """)

    parser.add_argument('-v', '--version', action='version', version=UIP_CLI_VERSION)

    cmd_type_subparsers = parser.add_subparsers(title="commands", dest='command_type', metavar='<command>')
    cmd_type_subparsers.required = True

    # init command setup
    setup_init_arg(cmd_type_subparsers)

    # template command setup
    setup_template_arg(cmd_type_subparsers)

    # build command setup
    setup_build_arg(cmd_type_subparsers)

    # upload command setup
    setup_upload_arg(cmd_type_subparsers)

    # push command setup
    setup_push_arg(cmd_type_subparsers)

    # pull command setup
    setup_pull_arg(cmd_type_subparsers)

    # download command setup
    setup_download_arg(cmd_type_subparsers)

    # clean command setup
    setup_clean_arg(cmd_type_subparsers)

    # task command setup
    setup_task_arg(cmd_type_subparsers)

    # template-list command setup (will be deprecated in two releases)
    setup_template_list_arg_deprecated(cmd_type_subparsers)

    if not args_list:
        parser.print_help()
    else:
        args = parser.parse_args(args_list)
        for f in validation_funcs:
            f(parser, args)
        parse_cli_args(args)
