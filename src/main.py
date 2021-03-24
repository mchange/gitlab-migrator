# -*- coding: utf-8 -*-

import os, sys, config, base
from users import Users
from groups import Groups
from groups_members import GroupsMembers
from projects import Projects
from repositories import Repositories
import time

# from clean import Clean

def execute(cfg):
	users = Users(cfg).run()
	base.storage('users', users)
	time.sleep(5)

	groups = Groups(cfg).run()
	base.storage('groups', groups)
	time.sleep(5)

	members = GroupsMembers(cfg, users, groups).run()
	base.storage('groups-members', members)
	time.sleep(10)

	projects = Projects(cfg, users['target'], groups['target']).run()
	base.storage('projects', projects)

	time.sleep(10)
	Repositories(cfg, projects['source']).run()

if __name__ == '__main__':
	env = sys.argv[1:]
	if env:
		env = env[0]
	else:
		env = 'test'

	tmppath = 'tmp'
	if not os.path.exists(tmppath):
		os.makedirs(tmppath)

	cfg = {
		'source': config.SOURCE,
		'target': config.TARGET.get(env, config.TARGET['test'])
	}

	print('Migrator configuration:')
	for key in cfg:
		cfg[key]['headers'] = { 'PRIVATE-TOKEN': cfg[key]['access_token'] }
		print('%s:' % key)
		print(cfg[key])
	cfg['per_page'] = 500

	# Clean()
	execute(cfg)
