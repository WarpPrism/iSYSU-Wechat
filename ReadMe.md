## iSYSU-Wechat ##

### 简介 ###

中山大学官方微信（公众号iSYSU），旨在为中大学子提供可靠，便利的一站式校园服务，主要有：
- 校园公众号
- 查询大厅，校园生活服务
- 推广H5小游戏，H5页面等

### 技术架构 ###

- 前端：Bootstrap3.3.5，cocos2d-js-v3.8，jquery2.1.4，移动端Web
- 后台：基于python的Tornado，Nginx作反向代理，supervisor作进程管理，多端口负载均衡。
- 数据库：MySQL关系型数据库
- 域名：isysu.sysu.edu.cn
- 服务器：学校提供的虚拟主机CentOS

### 项目结构 ###

- static:			包含静态文件， css, js, res/imgs, libs（依赖库）
- templates:		模板文件
- .idea: 			pycharm IDE 依赖
- server.py等 		服务器代码

### 项目进度 ###
1. 查询大厅
	- 教务查询
	- 校车查询
	- 图书馆查询
	- 宿舍查询
	- 自习室查询
	- 校历查询
2. Run SYSUer！

