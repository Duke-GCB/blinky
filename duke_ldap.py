import ldap

class DukeLdap:
  def __init__(self, hostname):
    self.ldap_conn = ldap.open("ldap.duke.edu")

  def member_uid(self, duke_id):
    l = self.ldap_conn
    r = l.search("dc=duke,dc=edu", ldap.SCOPE_SUBTREE, "duDukeID="+duke_id, ['uid'])
    result = l.result(r, 0)
    if result[0] == 100:
      return result[1][0][1]['uid'][0]
    else:
      return "PC_LOAD_LETTER"
