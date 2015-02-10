from grouper_ws import GrouperWS
from duke_ldap import DukeLdap

class Blinky:
  def __init__(self, ws_base_url, ws_account_id, ws_password, ldap_hostname):
    self.grouper = GrouperWS(ws_base_url, ws_account_id, ws_password)
    self.ldap = DukeLdap(ldap_hostname)

  def group_members(self, group_name):
    members = []
    for member in self.grouper.group_member_ids(group_name):
      m = {}
      m['id'] = member['id']
      m['uid'] = self.ldap.member_uid(member['id'])
      members.append(m)
    return members
