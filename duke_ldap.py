import logging
import ldap

class DukeLdap:
  def __init__(self, hostname):
    self.ldap_conn = ldap.open("ldap.duke.edu")

  def member(self, duke_id):
    member = {}
    attrs = ['uid']
    l = self.ldap_conn
    r = l.search("dc=duke,dc=edu", ldap.SCOPE_SUBTREE, "duDukeID="+duke_id, attrs)
    result = l.result(r, 0)
    logging.debug(result)
    if result[0] == 100:
      for attr in attrs:
        member[attr] = result[1][0][1][attr][0]
    return member
