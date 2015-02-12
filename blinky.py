import logging
import json
from grouper_ws import GrouperWS
from duke_ldap import DukeLdap

class Blinky:
  def __init__(self, ws_base_url, ws_account_id, ws_password, ldap_hostname):
    self.grouper = GrouperWS(ws_base_url, ws_account_id, ws_password)
    self.ldap = DukeLdap(ldap_hostname)

  def group_members(self, group_name):
    members = []
    for member in self.grouper.group_members(group_name):
      member.update(self.ldap.member(member['id']))
      members.append(member)
    logging.debug(json.dumps(members, indent=2))
    return members

  def group_delete_member(self, group_name, duke_id):
    return self.grouper.group_delete_member(group_name, duke_id)

  def group_add_member(self, group_name, duke_id):
    return self.grouper.group_add_member(group_name, duke_id)
