# 更新

## 升级

- **9.1.7**  升级到 **13.9.4**

- 新增分页处理
- 修复不同组下，同名项目同步问题
- 修复同名项目pull异常问题

## 注意

- User同步，不能同步用户状态（正常、禁用），默认都是正常状态
- 组权限	>= 组内项目权限

---



> Gitlab API : https://docs.gitlab.com/ee/api

# GitLab Community Edition数据迁移

使用`gitlab-ce` API进行私有仓库数据迁移，从`9.5.4`迁至`12.4.2`。因版本不同，无法使用`gitlab-rake`工具进行`backup`/`restore`。

## 配置

`src/config.py`:

- `SOURCE`: 老版本GitLab地址(端口`80`)与访问令牌

- `TARGET`: 新版本GitLab(`test`/`prod`)地址与访问令牌

## 迁移数据列表

- [X] Users
- [X] Groups
- [X] Group members
- [X] Projects
- [X] Repositories
- [ ] Issues
- [ ] Merge requests

## 用法

- 迁移
``` sh
$ python3 src/main.py [test | prod]
```

- 清除测试目标库中的数据
``` sh
$ python3 src/clean.py
```

