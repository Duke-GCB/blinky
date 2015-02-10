import json
import requests

class GrouperWS:
  def __init__(self, base_url, account_id, account_pass, verbose=False):
    self.base_url = base_url
    self.account_id = account_id
    self.account_pass = account_pass
    self.verbose = verbose

  def ws_get(self, url, root_node=None):
    result = json.loads(requests.get(self.base_url + url,auth=(self.account_id, self.account_pass)).content)
    if self.verbose:
      print json.dumps(result, indent=2)
    if root_node:
      return result[root_node]
    else:
      return result

  def subjects(self, url, root_node=None):
    return self.ws_get(url, root_node)['wsSubjects']

  def group_member_ids(self, group_name):
    return self.subjects('/groups/' + group_name +'/members', 'WsGetMembersLiteResult')

  def group_members(self, group_name):
    members = []
    subjects = self.subjects('/groups/' + group_name +'/members', 'WsGetMembersLiteResult')
    for subject in subjects:
      for member in self.subjects('/subjects/' + subject['id'], 'WsGetSubjectsResults'):
        members.append(member)
    return members
