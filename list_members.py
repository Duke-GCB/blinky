import ConfigParser
import os
import argparse
from grouper_ws import GrouperWS

parser = argparse.ArgumentParser(description='List the members of a group', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('group_name', help='is the name of the group including stems, e.g duke:gcb:security:admins')
parser.add_argument('--config', help='location of the config file', default=os.path.expanduser('~/.grouper_script.cfg'))
args = parser.parse_args()

config = ConfigParser.ConfigParser()
config.readfp(open(args.config))

ws_config = dict(config.items('GrouperWebServices'))
ws = GrouperWS(ws_config['base_url'], ws_config['account_id'], ws_config['account_password'])

subjects = ws.subjects('/groups/' + args.group_name +'/members', 'WsGetMembersLiteResult')
for subject in subjects:
  members = ws.subjects('/subjects/' + subject['id'], 'WsGetSubjectsResults')

  for member in members:
    print member['id'], member['name']
