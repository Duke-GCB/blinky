import ConfigParser
import os
import argparse
from grouper_ws import GrouperWS
import ldap

parser = argparse.ArgumentParser(description='List the members of a group', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('group_name', help='is the name of the group including stems, e.g duke:gcb:security:admins')
parser.add_argument('--config', help='location of the config file', default=os.path.expanduser('~/.grouper_script.cfg'))
args = parser.parse_args()

config = ConfigParser.ConfigParser()
config.readfp(open(args.config))

ws_config = dict(config.items('GrouperWebServices'))
ws = GrouperWS(ws_config['base_url'], ws_config['account_id'], ws_config['account_password'])

duke_ldap = ldap.open("ldap.duke.edu")
for member in ws.group_members(args.group_name):
  r = duke_ldap.search("dc=duke,dc=edu", ldap.SCOPE_SUBTREE, "duDukeID="+member['id'], ['uid'])
  ldap_result = duke_ldap.result(r,0)
  if ldap_result[0] == 100:
    print '{0}:{1}:{2}'.format(member['id'], ldap_result[1][0][1]['uid'][0], member['name'])
  else:
    print ":("
