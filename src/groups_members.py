# -*- coding: utf-8 -*-

import requests

class GroupsMembers(object):
	def __init__(self, cfg, users, groups):
		super(GroupsMembers, self).__init__()
		self.api = 'http://%s/api/v4/groups/%s/members?per_page=100'
		self.api_add = 'http://%s/api/v4/groups/%s/members'
		self.source = cfg['source']
		self.target = cfg['target']
		self.users = users
		self.groups = groups

	def run(self):
		members = self.index()
		self.add(members)

		return members

	def index(self):
		target_groups = self.groups['target']
		target_users = self.users['target']
		source_groups = self.groups['source']

		target_members = []
		# print("target_groups: ", target_groups)
		for group in source_groups:
			# print("current group:" , group)
			tgroup = next(x for x in target_groups if x['name'] == group['name'])
			resp = requests.get(
				self.api % (self.source['address'], group['id']),
				headers = self.source['headers'])
			source_members = resp.json()
			# print("source_members: ", source_members)
			for m in source_members:
				tm = next(x for x in target_users if x['username'] == m['username'])
				m['target_id'] = tm['id']
				m['target_username'] = tm['username']
			target_members.append({
				'id': group['id'],
				'name': group['name'],
				'target_id': tgroup['id'],
				'target_name': tgroup['name'],
				'members': source_members
			})

		return target_members

	def add(self, members):
		for gm in members:
			gid = gm['target_id']
			for m in gm['members']:
				data = {
					'id': gid,
					'user_id': m['target_id'],
					'access_level': m['access_level']
				}
				requests.post(
					self.api_add % (self.target['address'], gid),
					headers = self.target['headers'], 
					data = data)
