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

def ws_get(url):
  return json.loads(requests.get(base_url + url,auth=(account_id, account_pass)).content)

result = ws_get('/groups/' + args.group_name +'/members')

subjects = result['WsGetMembersLiteResult']['wsSubjects']
for subject in subjects:
  member = ws_get('/subjects/' + subject['id'])

  print member['WsGetSubjectsResults']['wsSubjects'][0]['id'], member['WsGetSubjectsResults']['wsSubjects'][0]['name']
