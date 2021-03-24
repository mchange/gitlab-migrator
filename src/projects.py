# -*- coding: utf-8 -*-

import requests

'''
分页： 	page		页码（默认：）1。
		per_page	每页要列出的项目数（默认值：20，最大值：100）。
'''
class Projects(object):
	def __init__(self, cfg, target_users, target_groups):
		super(Projects, self).__init__()
		self.api = 'http://%s/api/v4/projects'
		self.source = cfg['source']
		self.target = cfg['target']
		self.per_page = cfg['per_page']
		self.target_users = target_users
		self.target_groups = target_groups

		# self.users_map = {}
		# for u in target_users:
		# 	self.users_map['username'] = u['id']

		# self.group_map = {}
		# for u in target_users:
		# 	self.group_map['username'] = u['id']

	def run(self):
		source = self.get()
		target = self.inserts(source)
		
		return { 'source': source, 'target': target }

	def get(self):
		# 分页处理
		hasNext = True
		currentPage = 1
		projects = []
		while hasNext is True :
			project = requests.get(
				self.api % self.source['address'], 
				headers = self.source['headers'],
				params = { 'order_by': 'updated_at', 'per_page': self.per_page, 'page':currentPage }).json()
			
			currentPage = currentPage + 1

			# print('project: ', project)
			
			if len(project) < 1 :
				hasNext = False
			else:
				projects = projects + project


		print('Total projects:', len(projects))

		return projects

	def inserts(self, projects):
		new_projects = []
		# print("projects: ", projects)
		print("target_groups: ", self.target_groups)
		for project in projects:
			npn = project['namespace']['path']
			print('namespace: ', project['namespace'])
			try:
				np = next(x for x in self.target_groups if x['path'] == npn)

				data = {
					"name": project['name'],
					"path": project['path'],
					"namespace_id": np['id'],
					"description": project['description'],
					"visibility": project['visibility'],
					"lfs_enabled": project['lfs_enabled']
				}
				resp = requests.post(
					self.api % self.target['address'], 
					headers = self.target['headers'], 
					data = data)
				new_projects.append(resp.json())
			except Exception as e:
				print(e)
				npn = project['namespace']['name']
				np = next(x for x in self.target_users if x['username'] == npn)

				data = {
					"name": project['name'],
					"path": project['path'],
					"user_id": np['id'],
					"description": project['description'],
					"visibility": project['visibility'],
					"lfs_enabled": project['lfs_enabled']
				}
				resp = requests.post(
					'%s/user/%s' % (self.api % self.target['address'], np['id']), 
					headers = self.target['headers'], 
					data = data)
				new_projects.append(resp.json())
	

		print('Create new project: %d' % len(new_projects))

		return new_projects
