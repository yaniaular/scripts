import module
import config
import branch 
from module import Module
from config import Config
from branch import Branch 

import os
import argparse
import argcomplete

def dir_full_path(path):
    """
    Calculate the abosulte path for a given path. It get the absolute path
    taking into account the current path were the tool is running.
    @param path: a directory path
    @return: the absolute path of a directory.
    """
    my_path = os.path.abspath(path)
    if not os.path.isdir(my_path):
        msg = 'The directory given did not exist %s' % my_path
        raise argparse.ArgumentTypeError(msg)
    return my_path

def argument_parser(args_list=None):
    """
    This function create the help command line and manage and filter the
    parameters of this program (default values, choices values)
    """
    my_config = Config()
    parser = argparse.ArgumentParser(
        prog='oerpmodule',
        description='Create new openerp module structure and basic files.',
        epilog="""
Openerp Developer Comunity Tool
Development by Vauxoo Team (lp:~vauxoo)
Coded by Katherine Zaoral <kathy@vauxoo.com>.
Source code at lp:~katherine-zaoral-7/+junk/oerp_module.""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparsers = parser.add_subparsers(
        description=('Valid actions over a module than can be done with'
            ' oerpmodule.'),
        dest='action',
        help='subcommands help')

    # create sub parser for create action
    create_parser = subparsers.add_parser(
        'create',
        help='Inicializate module. Create new directory with basic files.')
    create_paser = add_common_options(create_parser, my_config)
    create_paser.add_argument(
        '--add-init-data',
        metavar='CSV_DIR',
        type=dir_full_path,
        help=('path where the csv data it is. Note: This options depends on'
              ' the csv2xml python module'))
    create_paser.add_argument(
        '--company-name',
        metavar='COMPANY_NAME',
        type=str,
        help=('Used for the creating of on the fly csv records with a custom'
              ' xml id with the company prefix (required for csv2xml)'))

    # create sub parser for branch action
    branch_parser = subparsers.add_parser(
        'branch',
        help='Create a new module using a branch.')
    branch_paser = add_common_options(branch_parser, my_config)

    branch_parser.add_argument(
        '-r', '--parent_repo',
        metavar='PARENT_REPO',
        type=str,
        required=True,
        choices=my_config.get_repositories_names(),
        help=('The name of repository from will be create the new module. To '
              'look the repository list use oerpmodule config -l.'))

    branch_group = branch_parser.add_argument_group('New Branch Name options', (
        'This way you can configure the new branch name.'))

    branch_group.add_argument(
        '-s', '--branch-suffix',
        metavar='DEVELOPER_ACRONYM',
        type=str,
        help=str('Generally developer acronym name. It use when creating the'
                 ' branch for identify the team user owner in a simply way,'
                 ' It use is recommended.'))
    branch_group.add_argument(
        '-ov', '--oerp-version',
        metavar='VERSION',
        type=str,
        choices=my_config._oerp_version_list,
        help='Openerp version number')

    branch_parser.set_defaults(
        oerp_version='7.0',
        parent_repo='addons-vauxoo')

    # create sub parser for append action
    append_parser = subparsers.add_parser(
        'append', 
        help='Append a file to the module.')
    append_paser = add_common_options(append_parser, my_config)

    append_parser.add_argument(
        'append_file',
        metavar='FILE_TYPE',
        type=str,
        choices=['model', 'wizard'],
        help='The type of file you want to append.')
    append_parser.add_argument(
        'file_name',
        metavar='FILE_NAME',
        type=str,
        help='the name of the new model or wizard file that will be created.')

    # create sub parser for config action
    config_parser = subparsers.add_parser(
        'config', 
        help='Set and check the oerpmodule config')
    config_parser.add_argument(
        '-l', '--list-repositories', action='store_true',
        help='List the configurate repositories.')

    argcomplete.autocomplete(parser)
    args = parser.parse_args(args=args_list)
    check_inclusive_args(args)
    return args.__dict__

def check_inclusive_args(args):
    """
    Check the Inclusive arguments and introduce a parser error.
    """
    if args.add_init_data and not args.company_name:
        parser.error(' the --add-init-data requires --company-name option.')
    return True

def add_common_options(subparser, my_config):
    """
    I recive a parser object that repersent a subparser in this script to add
    it the common options needed. The subparser that share this common options
    are [create, append, branch] subparsers. The common options are:
    [module_name, module_developers, module_planners, module_auditors, dir].
    @return: the subparser object with the common arguments added.
    """
    subparser.add_argument(
        'module_name',
        metavar='MODULE_NAME',
        type=str,
        help='name of the module to create.')
    subparser.add_argument(
        '-d', '--module-developers',
        metavar='DEVELOPERS_INFO',
        type=str,
        help=str('A string with the module developers information. The format'
                 ' of this string is \'First Developer Name'
                 ' <developer@mail.com>, Second Developer Name'
                 ' <developerX@mail.com>\''),
        required=True)
    subparser.add_argument(
        '-p', '--module-planners',
        metavar='PLANNERS_INFO',
        type=str,
        help=str('A string with the module planners information. The format'
                 ' of this string is \'First Planner Name'
                 ' <planner@mail.com>, Second Planner Name'
                 ' <plannerX@mail.com>\''),
        required=True)
    subparser.add_argument(
        '-t', '--module-auditors',
        metavar='AUDITORS_INFO',
        type=str,
        help=str('A string with the module auditors information. The format'
                 ' of this string is \'First Auditor Name'
                 ' <auditor@mail.com>, Second Auditor Name'
                 ' <auditorX@mail.com>\''),
        required=True)
    subparser.add_argument(
        '-dir', '--destination-folder',
        metavar='DIR',
        type=dir_full_path,
        default=my_config.get_current_path(),
        help='name of the folder where to put the module')
    return subparser

def run(args):
    """
    run the corresponding action
    """
    my_config = Config()
    if args['action'] == 'config':
        args['list_repositories'] and my_config.print_repositories()
    else:
        module_obj = Module(
            args['module_name'], args['module_developers'],
            args['module_planners'],
            args['module_auditors'], folder=args['destination_folder'],
            init_data=args['add_init_data'], company_name=args['company_name'])
        if args['action'] == 'branch':
            branch_obj = Branch(
                module_obj, args['branch_suffix'], args['parent_repo'],
                args['oerp_version'], args['destination_folder'])
            branch_obj.create_branch()
            module_obj.create(branch_obj)
        elif args['action'] == 'create':
            module_obj.create()
        elif args['action'] == 'append':
            module_obj.append(args['append_file'], args['file_name'])

        #~ module_obj.branch_changes_apply()
    return True

def confirm_run(args):
    """
    Manual confirmation before runing the script. Very usefull.
    """
    print'\n... Configuration of Parameters Set'
    for (parameter, value) in args.iteritems():
        print '%s = %s' % (parameter, value)

    confirm_flag = False
    while confirm_flag not in ['y', 'n']:
        confirm_flag = raw_input(
            'Confirm the run with the above parameters? [y/n]: ')
        if confirm_flag == 'y':
            print 'The script parameters were confirmed by the user'
        elif confirm_flag == 'n':
            print 'The user cancel the operation'
            exit()
        else:
            print 'The entry is not valid, please enter y or n.'
    return True

def main():
    args = argument_parser()
    confirm_run(args)
    run(args)

