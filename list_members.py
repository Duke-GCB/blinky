import ConfigParser
import os
import argparse
import json
import requests

parser = argparse.ArgumentParser(description='List the members of a group', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('group_name', help='is the name of the group including stems, e.g duke:gcb:security:admins')
parser.add_argument('--config', help='location of the config file', default=os.path.expanduser('~/.grouper_script.cfg'))
args = parser.parse_args()

config = ConfigParser.ConfigParser()
config.readfp(open(args.config))

account_id = config.get('GrouperWebServices','account_id')
account_pass = config.get('GrouperWebServices','account_password')
base_url = config.get('GrouperWebServices','base_url')

def ws_get(url, root_node=None):
  result = json.loads(requests.get(base_url + url,auth=(account_id, account_pass)).content)
  if root_node:
    return result[root_node]
  else:
    return result

def ws_dump(url, root_node=None):
  return json.dumps(ws_get(url, root_node), indent=2)

def ws_subjects(url, root_node=None):
  return ws_get(url, root_node)['wsSubjects']

subjects = ws_subjects('/groups/' + args.group_name +'/members', 'WsGetMembersLiteResult')
for subject in subjects:
  members = ws_subjects('/subjects/' + subject['id'], 'WsGetSubjectsResults')

  for member in members:
    print member['id'], member['name']
