# School_profile
## 1. Pycharm运行配置说明
因为flask的app对象被封装在了web/\__init__.py中的工厂方法create_app中，所以需要进行一些设置才可以运行
>```
>1. 在Pycharm中对Flask server设置（可断点调试）：
>>   1. 打开Edit Configuration
>>   2. 设置Target type => Script path。
>>   3. 设置Target => wsgi.py的完整路径。
>2. 在cmd中设置（无法断点调试）：  
>>   1. set FLASK_APP=web
>>   2. flask run  
>```
>flask的自动搜索机制会自动从FLASK_APP的值定义的模块中寻找名称为create_app()或make_app()的工厂函数
## 2. Docker部署
>使用docker-compose生成flask和nginx容器，flask容器开放了5000端口，nginx容器接收请求
>并转发给flask容器，nginx绑定80端口。  
>需要安装 docker docker-compose
>```
>docker-compose up # 前台运行
>docker-compose up -d # 后台运行
>docker-compose build  # 创建镜像
>docker-compose rm # 删除当前容器 需要再次确认
>```
## 3. 第三方库
>### 1. flask相关库
>1. [Bootstrap-Flask](https://bootstrap-flask.readthedocs.io/en/latest/)  
>该库是bootstrap4的封装，提供了若干个jinja2函数。
>2. [Flask-login](https://flask-login.readthedocs.io/en/latest/)  
>简化用户的登录
>3. [CSRFProtect](http://www.pythondoc.com/flask-wtf/csrf.html)  
>Flask-WTF内置的扩展，单独使用时实现对程序的全局CSRF保护。主要提供了
>生成和验证CSRF令牌的函数。
>如果是同步请求，请在form中添加：
>```
><input type="hidden" name="csrf_token" value="{{csrf_token()}}"/>
>```
>验证失败返回400
>异步加载时需要在html文件中添加：
>```
>    let csrf_token = "{{ csrf_token() }}";
>    //在确保请求不属于GET HEAD OPTIONS TRACE，并且发向站内，才设置csrf_token
>    $.ajaxSetup({
>        beforeSend: function (xhr, settings) {
>            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain){
>                xhr.setRequestHeader("X-CSRFToken", csrf_token);
>            }
>        }
>    });
>```
>4. [flask-sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
>ORM，一般使用类进行操作.当使用多个数据库时，首先需要进行配置：
>```
># 默认数据库
>SQLALCHEMY_DATABASE_URI = '...'
># 其他数据库
>SQLALCHEMY_BINDS = {
>    'data_mining': '...'
>}
>```
>在构建对象类时，可以通过指定__bind_key__ 来设置当前所使用的数据库,比如：
>```
>class Applicant(db.Model):
>   __bind_key__ = 'data_mining'
>   # ...
>```
>若没有，则使用默认的数据库
>另外一个使用的场景则是使用原生SQL语句，例如utils.db中的  
>```
>def select(sql, params=None, fetch='all', convert_list=False, bind=None)
>```
>当bind为None时，则使用默认的数据库，否则同上。
>5. [flask-moment](https://github.com/miguelgrinberg/flask-moment/)
> 转换datetime，比如 "3天前"
>### 2. js库
>1. [Bootstrap4](https://v4.bootcss.com/docs/getting-started/introduction/)  
>页面整体风格相关
>2. [select2](https://select2.org/getting-started/basic-usage)  
>下拉多选框
>3. [Datetime Picker](https://www.malot.fr/bootstrap-datetimepicker/)  
>具体到时间的选择器
>4. [feather](https://feathericons.com/)  
>图标库
>5. [CKEditor](https://ckeditor.com/docs/ckeditor5/latest/builds/guides/integration/configuration.html)  
>富文本编辑框
## 4. 测试
>1. [unittest](https://docs.python.org/3/library/unittest.html)    
>python基础库，用于单元测试和集成测试
>2. [selenium](https://selenium-python.readthedocs.io/)  
>模拟浏览器，用于搭配unittest进行集成测试  
>3. [flask-session-cookie-manager](https://github.com/noraj/flask-session-cookie-manager)  
>编解码 cookie

## 5. 注意事项
> 在使用jinja2等服务器模板引擎时，避免使用字符串拼接模板字符串，以造成
>SSTI（服务器模板注入）