import logging
import ldap

class DukeLdap:
  def __init__(self, hostname):
    self.ldap_conn = ldap.open("ldap.duke.edu")

  def search(self, filter, attrs=[]):
    member = {}
    l = self.ldap_conn
    r = l.search("dc=duke,dc=edu", ldap.SCOPE_SUBTREE, filter, attrs)
    result = l.result(r, 0)
    logging.debug(result)
    if result[0] == 100:
      for attr in result[1][0][1].keys():
        member[attr] = result[1][0][1][attr][0]
    return member

  def member(self, duke_id=None, net_id=None):
    member = {}
    if duke_id:
      member = self.search("duDukeID="+duke_id, ['uid'])
    elif net_id:
      member = self.search("uid="+net_id, ['duDukeID'])
    return member
