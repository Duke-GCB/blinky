import logging
import json

from grouper_ws import GrouperWS
from duke_ldap import DukeLdap


class Blinky(object):
    """
    Allows a user to view and manage data in both duke ldap and group manager.
    """
    def __init__(self, ws_base_url, ws_account_id, ws_password, ldap_hostname):
        """
        :param ws_base_url: str: url to grouper
        :param ws_account_id: str: integer id of the user we will use for grouper authentication
        :param ws_password: str: password of the user we will user for grouper authentication
        :param ldap_hostname: str: duke ldap domain name
        """
        self.grouper = GrouperWS(ws_base_url, ws_account_id, ws_password)
        self.ldap = DukeLdap(ldap_hostname)

    def group_members(self, group_name):
        members = []
        for member in self.grouper.group_members(group_name):
            member.update(self.ldap.member(member['id']))
            members.append(member)
        logging.debug(json.dumps(members, indent=2))
        return members

    def member_groups(self, net_id):
        member = self.ldap.member(net_id=net_id)
        if member['duDukeID']:
            return self.grouper.member_groups(member['duDukeID'])

    def group_delete_member(self, group_name, net_id):
        member = self.ldap.member(net_id=net_id)
        if member['duDukeID']:
            return self.grouper.group_delete_member(group_name, member['duDukeID'])

    def group_add_member(self, group_name, net_id):
        member = self.ldap.member(net_id=net_id)
        if member['duDukeID']:
            return self.grouper.group_add_member(group_name, member['duDukeID'])

    def group_save(self, group_name):
        return self.grouper.group_save(group_name)

    def stems(self, stem_name):
        stems = self.grouper.stems(stem_name)
        return [stem['name'] for stem in stems['stemResults']]
