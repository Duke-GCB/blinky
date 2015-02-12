import ConfigParser
import os
import argparse
import logging
from blinky import Blinky

def __main__():
  parser = argparse.ArgumentParser(description='Grouper mutation that can see ldap with its third eye.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parent_parser = argparse.ArgumentParser(add_help=False)
  parent_parser.add_argument('--config', help='location of the config file', default=os.path.expanduser('~/.grouper_script.cfg'))
  parent_parser.add_argument('--debug', help='display information to aid in debugging', action='store_true')

  subparsers = parser.add_subparsers(help='sub-command help')

  group_members_parser = subparsers.add_parser('group_members', help='group_members help', parents=[parent_parser])
  group_members_parser.add_argument('group_name', help='is the name of the group including stems, e.g duke:gcb:security:admins')
  group_members_parser.set_defaults(func=group_members)

  group_delete_member_parser = subparsers.add_parser('delete_member', help='delete_member help', parents=[parent_parser])
  group_delete_member_parser.add_argument('group_name', help='is the name of the group including stems, e.g duke:gcb:security:admins')
  group_delete_member_parser.add_argument('duke_id', help='is numeric duke unique id to delete from the group')
  group_delete_member_parser.set_defaults(func=group_delete_member)

  group_add_member_parser = subparsers.add_parser('add_member', help='add_member help', parents=[parent_parser])
  group_add_member_parser.add_argument('group_name', help='is the name of the group including stems, e.g duke:gcb:security:admins')
  group_add_member_parser.add_argument('duke_id', help='is numeric duke unique id to add from the group')
  group_add_member_parser.set_defaults(func=group_add_member)

  args = parser.parse_args()

  config = ConfigParser.ConfigParser()
  config.readfp(open(args.config))

  if args.debug:
    logging.basicConfig(format='%(levelname)s[%(module)s.%(funcName)s]:%(message)s', level=logging.DEBUG)

  ws_config = dict(config.items('GrouperWebServices'))
  ldap_config = dict(config.items('DukeLdap'))
  duke_blinky = Blinky(
      ws_base_url = ws_config['base_url'], 
      ws_account_id = ws_config['account_id'], 
      ws_password = ws_config['account_password'],
      ldap_hostname = ldap_config['hostname'])
  args.func(duke_blinky, args)

def group_members(duke_blinky, args):
  for member in duke_blinky.group_members(args.group_name):
    print member['id']+':'+member['uid']
def group_delete_member(duke_blinky, args):
  print duke_blinky.group_delete_member(args.group_name, args.duke_id)
def group_add_member(duke_blinky, args):
  print duke_blinky.group_add_member(args.group_name, args.duke_id)

__main__()
