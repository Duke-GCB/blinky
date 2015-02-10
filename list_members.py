import ConfigParser
import os
import argparse
from blinky import Blinky

parser = argparse.ArgumentParser(description='List the members of a group', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('group_name', help='is the name of the group including stems, e.g duke:gcb:security:admins')
parser.add_argument('--config', help='location of the config file', default=os.path.expanduser('~/.grouper_script.cfg'))
parser.add_argument('--verbose', help='display data returned from ldap and web services', action='store_true')
args = parser.parse_args()

config = ConfigParser.ConfigParser()
config.readfp(open(args.config))

ws_config = dict(config.items('GrouperWebServices'))
ldap_config = dict(config.items('DukeLdap'))
duke_blinky = Blinky(
    ws_base_url = ws_config['base_url'], 
    ws_account_id = ws_config['account_id'], 
    ws_password = ws_config['account_password'],
    ldap_hostname = ldap_config['hostname'],
    verbose=args.verbose)

for member in duke_blinky.group_members(args.group_name):
  print member['id']+':'+member['uid']
