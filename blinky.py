from grouper_ws import GrouperWS
from duke_ldap import DukeLdap

class Blinky:
  def __init__(self, ws_base_url, ws_account_id, ws_password, ldap_hostname, verbose=False):
    self.grouper = GrouperWS(ws_base_url, ws_account_id, ws_password, verbose)
    self.ldap = DukeLdap(ldap_hostname, verbose)
    self.verbose = verbose

  def group_members(self, group_name):
    members = []
    for member in self.grouper.group_members(group_name):
      member.update(self.ldap.member(member['id']))
      members.append(member)
    if self.verbose:
      print members
    return members
