## iSYSY-Wechat ##

### 简介 ###

中山大学官方微信号服务的相关页面，如查询大厅，H5小游戏等等

### 技术架构 ###

- 后端服务器：基于python的Tornado
- 数据库：未使用，待定
- 前端：Bootstrap3， cocos2d-JS游戏框架， jquery

### 运行方法 ###

~~~
python server.py
查询大厅：localhost:8000/
第一个游戏： localhost:8000/game/
~~~

### 项目结构 ###

- static: 包含静态文件， css, js, res/imgs, libs（依赖库）
- templates: 模板文件
- .idea: pycharm IDE 依赖
- server.py

### 未完成任务 ###

- 小游戏
- 校历查询
- 自习室查询
- AND SO ON T_T。。。
