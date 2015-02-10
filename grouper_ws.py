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

  def ws_subjects(self, url, root_node=None):
    return self.ws_get(url, root_node)['wsSubjects']

  def group_members(self, group_name):
    return self.ws_subjects('/groups/' + group_name +'/members', 'WsGetMembersLiteResult')
  def subjects(self, subject_id):
    return self.ws_subjects('/subjects/' + subject_id, 'WsGetSubjectsResults')

  def group_members_subjects(self, group_name):
    subjects = []
    members = self.group_members(group_name)
    for member in members:
      for subject in self.subjects(member['id']):
        subjects.append(subject)
    return subjects
