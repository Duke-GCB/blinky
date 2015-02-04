import json
import requests

class GrouperWS:
  def __init__(self, base_url, account_id, account_pass):
    self.base_url = base_url
    self.account_id = account_id
    self.account_pass = account_pass

  def ws_get(self, url, root_node=None):
    result = json.loads(requests.get(self.base_url + url,auth=(self.account_id, self.account_pass)).content)
    if root_node:
      return result[root_node]
    else:
      return result

  def ws_dump(self, url, root_node=None):
    return json.dumps(self.ws_get(url, root_node), indent=2)

  def subjects(self, url, root_node=None):
    return self.ws_get(url, root_node)['wsSubjects']
