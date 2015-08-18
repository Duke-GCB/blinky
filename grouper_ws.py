import logging
import json

import requests


class GrouperWS:
    def __init__(self, base_url, account_id, account_pass):
        self.base_url = base_url
        self.account_id = account_id
        self.account_pass = account_pass

    def ws_request(self, method, url, root_node=None):
        result = json.loads(
            requests.request(method, self.base_url + url, auth=(self.account_id, self.account_pass)).content)
        logging.debug(json.dumps(result, indent=2))
        if root_node:
            return result[root_node]
        else:
            return result

    def ws_get(self, url, root_node=None):
        return self.ws_request('GET', url, root_node)

    def ws_delete(self, url, root_node=None):
        return self.ws_request('DELETE', url, root_node)

    def ws_put(self, url, root_node=None):
        return self.ws_request('PUT', url, root_node)

    def ws_subjects(self, url, root_node=None):
        return self.ws_get(url, root_node)['wsSubjects']

    def ws_groups(self, url, root_node=None):
        return self.ws_get(url, root_node)['wsGroups']

    def group_members(self, group_name):
        return self.ws_subjects('/groups/' + group_name + '/members', 'WsGetMembersLiteResult')

    def member_groups(self, subject_id):
        return self.ws_groups('/subjects/' + subject_id + '/groups', 'WsGetGroupsLiteResult')

    def subjects(self, subject_id):
        return self.ws_subjects('/subjects/' + subject_id, 'WsGetSubjectsResults')

    def group_delete_member(self, group_name, duke_id):
        return self.ws_delete('/groups/' + group_name + '/members/' + duke_id, 'WsDeleteMemberLiteResult')

    def group_add_member(self, group_name, duke_id):
        return self.ws_put('/groups/' + group_name + '/members/' + duke_id, 'WsAddMemberLiteResult')

    def group_members_subjects(self, group_name):
        subjects = []
        members = self.group_members(group_name)
        for member in members:
            for subject in self.subjects(member['id']):
                subjects.append(subject)
        return subjects
