#!/usr/bin/env python
import ConfigParser
import os
import argparse
import logging

from blinky import Blinky


def __main__():
    default_config_location = os.path.expanduser('~/.blinky.cfg')
    parser = argparse.ArgumentParser(description='Grouper mutation that can see ldap with its third eye.')

    common_args = argparse.ArgumentParser(add_help=False)
    common_args.add_argument('--config', help='location of the config file', default=default_config_location)
    common_args.add_argument('--debug', help='display information to aid in debugging', action='store_true')

    group_arg = argparse.ArgumentParser(add_help=False)
    group_arg.add_argument('group_name', help='is the name of the group including stems, e.g duke:gcb:security:admins')

    member_arg = argparse.ArgumentParser(add_help=False)
    member_arg.add_argument('net_id', help='is Duke net id to use')

    stem_arg = argparse.ArgumentParser(add_help=False)
    stem_arg.add_argument('stem_name', help='Stem Name (e.g. abc:def)')

    subparsers = parser.add_subparsers(help='sub-command help')

    subparsers.add_parser('group_members',
                          help='list members for group name',
                          parents=[common_args, group_arg],
                          formatter_class=argparse.ArgumentDefaultsHelpFormatter
                          ).set_defaults(func=group_members)

    subparsers.add_parser('member_groups',
                          help='list gropus for net id',
                          parents=[common_args, member_arg],
                          formatter_class=argparse.ArgumentDefaultsHelpFormatter
                          ).set_defaults(func=member_groups)

    subparsers.add_parser('delete_member',
                          help='delete member from group',
                          parents=[common_args, group_arg, member_arg],
                          formatter_class=argparse.ArgumentDefaultsHelpFormatter
                          ).set_defaults(func=group_delete_member)

    subparsers.add_parser('add_member',
                          help='add member to group',
                          parents=[common_args, group_arg, member_arg],
                          formatter_class=argparse.ArgumentDefaultsHelpFormatter
                          ).set_defaults(func=group_add_member)

    subparsers.add_parser('group_save',
                          help='create/save a group',
                          parents=[common_args, group_arg],
                          formatter_class=argparse.ArgumentDefaultsHelpFormatter
                          ).set_defaults(func=group_save)

    subparsers.add_parser('find_stems',
                          help='Find stems matching a name',
                          parents=[common_args, stem_arg],
                          formatter_class=argparse.ArgumentDefaultsHelpFormatter
                          ).set_defaults(func=find_stems)

    args = parser.parse_args()

    config = ConfigParser.ConfigParser()
    config.readfp(open(args.config))

    if args.debug:
        logging.basicConfig(format='%(levelname)s[%(module)s.%(funcName)s]:%(message)s', level=logging.DEBUG)

    ws_config = dict(config.items('GrouperWebServices'))
    ldap_config = dict(config.items('DukeLdap'))
    duke_blinky = Blinky(
        ws_base_url=ws_config['base_url'],
        ws_account_id=ws_config['account_id'],
        ws_password=ws_config['account_password'],
        ldap_hostname=ldap_config['hostname'])
    args.func(duke_blinky, args)


def group_members(duke_blinky, args):
    for member in duke_blinky.group_members(args.group_name):
        print member['id'] + ':' + member['uid']


def member_groups(duke_blinky, args):
    for group in duke_blinky.member_groups(args.net_id):
        print group['name']


def group_delete_member(duke_blinky, args):
    print duke_blinky.group_delete_member(args.group_name, args.net_id)


def group_add_member(duke_blinky, args):
    print duke_blinky.group_add_member(args.group_name, args.net_id)

def group_save(duke_blinky, args):
    print duke_blinky.group_save(args.group_name)


def find_stems(duke_blinky, args):
    for stem_name in duke_blinky.stems(args.stem_name):
        print stem_name

__main__()
