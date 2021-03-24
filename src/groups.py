# -*- coding: utf-8 -*-

import requests

class Groups(object):
	def __init__(self, cfg):
		super(Groups, self).__init__()
		# 结果是分页返回，默认20个，最大支持100个，设置per_page=100，如果组超过100，请自行实现分也请求
		self.api = 'http://%s/api/v4/groups?per_page=100'
		self.api_add = 'http://%s/api/v4/groups'
		self.source = cfg['source']
		self.target = cfg['target']

	def run(self):
		source = self.get()
		target = self.inserts(source)
		
		return { 'source': source, 'target': target }

	def get(self):
		resp = requests.get(
			self.api % self.source['address'], 
			headers = self.source['headers'])

		groups = sorted(resp.json(), key = lambda x:x['id'], reverse = False)

		print('Total groups: %d' % len(groups))
		# print('Total groups: ', groups)
		return groups

	def inserts(self, groups):
		new_groups = []
		# 存放新旧id的映射关系，处理子群组的关联关系
		old_new_groups_map = {}
		for group in groups:
			old_new_groups_map[group['id']] = 0
			data = {
				"name": group['name'],
				"path": group['path'],
				"description": group['description'],
				"visibility": group['visibility'],
				"lfs_enabled": group['lfs_enabled']
			}
			if group['parent_id'] is not None:
				# print('check parent_id:', group['parent_id'])
				data['parent_id'] = old_new_groups_map[group['parent_id']]
			resp = requests.post(
				self.api_add % self.target['address'], 
				headers = { 'PRIVATE-TOKEN': self.target['access_token'] }, 
				data = data)
			# print('add group result:', resp.json())
			old_new_groups_map[group['id']] = resp.json().get('id')
			new_groups.append(resp.json())


		print('Create new group: %d' % len(new_groups))

		return new_groups


		'''
		子群组和项目的权限不同，需要统一
		current group: {'id': 28, 'name': 'alpha', 'path': 'alpha', 'description': '内部项目孵化', 'visibility': 'internal', 'lfs_enabled': True, 'avatar_url': None, 'web_url': 'http://192.168.0.7/groups/pay/alpha', 'request_access_enabled': False, 'full_name': 'pay / alpha', 'full_path': 'pay/alpha', 'parent_id': 12}
		'''
