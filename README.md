#框架介绍
采用Flask，模板引擎jinjia2，数据库orm用Sqlachemy

#结构介绍


##路由


默认get, post, delete, put方法
```
#四个参数分别是，url，View类名，control实例，允许的请求方式
urls = [
    ("user", User, user_ctl, ["GET", "POST"]),
]
for i in restful_urls.urls:
    _methods = methods
    if len(i) == 4:
        _methods = i[3]
    url_prefix = "/%s" % i[0]
    app.add_url_rule(url_prefix, url_prefix, dispatch(i), methods=_methods)
def dispatch(item):
    def _dispatch(**kwargs):
        obj = item[1]
        kwargs["controller_obj"] = item[2]
        return obj(**kwargs).dispatch()
    return _dispatch
```
采用循环的方法类设置路由，method来控制请求方式

##MVC结构
###Model
数据库采用Sqlachemy所有model直接采用其对用的ORM
```
class UserModel(Base):
    __tablename__ = 'user'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(256), nullable=False, server_default='')
    password = Column(String(256), nullable=False, server_default='')
    avatar = Column(String(256), nullable=False, server_default='')
    create_time = Column(DateTime(), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    # 更新时间
    update_time = Column(DateTime(), nullable=False,
                         server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


if settings.CREATE_TABLE:
    create_table("user")
```

###View
所有路由都从view进入，经过dispatch函数分发，所有的view继承Baseview
不同的请求方法，进入到不同的函数，并返回
```
        elif request.method == "POST":
            action = self._input.get("action", None)
            if action:
                func = getattr(self, "post_action_%s" % action, None)
                if func:
                    return func()
                else:
                    return render_template("404.html")
            else:
                return self.post()
        elif request.method == "PUT":
            return self.put()
        elif request.method == "DELETE":
            return self.delete()
```
子类只需要实现对应方法，如果不重写。则会返回改Model对应数据表的数据

###Control
control里面封装了所有对数据库操作的方法。
```
def filter_item(self, **kwargs)
def update_item(self, **kwargs)
def delete_item(self, **kwargs)
def new_item(self, **kwargs)
def do_filter(self, **kwargs)#查询条件过滤
```
子类只需要继承即可实例化即可
```
#参数为UserModel的类名
user_ctl = UserController(UserModel)

```
###Template
模板渲染用jinjia，所以充分利用base，macros
所有html继承base，这里把style,和警告框统一在base里面引入
```
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}{% endblock %}</title>
	<script src="/static/jquery.min.js"></script>
</head>
<body>
    <div class="warn_modal"></div>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
            <ul class="flashes">
            {% for message in messages %}
            <li>{{ message }}</li>
            {% endfor %}
            </ul>
        {% endif %}
    {% endwith %}
    {% block content %}{% endblock %}
    {% endblock %}
</body>
</html>

```
macro主要用来定义控件标签，统一化




