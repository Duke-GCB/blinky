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

account_id = config.get('GrouperWebServices','account_id')
account_pass = config.get('GrouperWebServices','account_password')
base_url = config.get('GrouperWebServices','base_url')
ws = GrouperWS(base_url, account_id, account_pass)

subjects = ws.subjects('/groups/' + args.group_name +'/members', 'WsGetMembersLiteResult')
for subject in subjects:
  members = ws.subjects('/subjects/' + subject['id'], 'WsGetSubjectsResults')

  for member in members:
    print member['id'], member['name']
