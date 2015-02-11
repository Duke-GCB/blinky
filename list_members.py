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

__main__()
