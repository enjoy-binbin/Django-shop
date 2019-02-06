大四毕业设计课题
===========================

#### 系统主要是针对实现了对网上超市购物的自动化管理，它使得商品的管理工作走向全面自动化、规范化，且通过网络廉价快捷的通讯手段，消除时间与空间带来的障碍，从而大大的节约了交易成本，扩大了交易范围。构件一个网络购物系统能让我们更适应当今社会快节奏生活，使得顾客足不出户便可以方便轻松地选购自己喜欢的商品。
#### 系统主要是为用户提供网上注册、网上浏览商品信息、网上购物的功能以及商家后台管理：包括添加商品、删除商品和修改商品等重要功能，这些功能，极大地提高了购物的效率。
#### 开发一套网上商城购物系统,包括了用户账号管理、用户信息管理、超市商品管理、超市后台管理、添加商品信息、修改商品信息、删除商品信息、用户注册，用户查看商品信息、用户购买商品、等重要的功能。系统逐步展开设计，包括系统分析，系统总体设计，系统的详细设计等，最后对系统进行全面的测试。


## TOLearn: Django通用view，中高级用法
## 我的开发环境:  先简单的来，前后端不分离。时间 18年12月
1. win10 64位
2. python 3.6
3. Django 2.1
4. Mysql 5.6
5. PyCharm 2018.1
6. xadmin后台： `admin 123456`

## 运行方法(下面有展示页)：
1. 安装依赖 (最好新建个虚拟环境)
	* pip install -Ur requirements -i https://pypi.douban.com/simple
2. 运行
	* 自行修改 `binshop/settings.py` 里的数据库配置:
			
			DATABASES = {
			    'default': {
			        'ENGINE': 'django.db.backends.mysql',
			        'NAME': 'binshop',
			        'USER': 'root',
			        'PASSWORD': '1123',
			        'HOST': '127.0.0.1'
			    }
			}
	* 创建数据库 `create database binshop;`
	* 在终端下进行数据迁移:
	
			./manage.py makemigrations
			./manage.py migrate
	* 根据需要用Navicat导入目录下的sql文件
	* 运行： `./manage.py runserver 0.0.0.0:8000`
	* 浏览器打开: **http://127.0.0.1:8000/**
3. 配置项 (更多设置项看settings)
	* 后台入口: `http://127.0.0.1:8000/xadmin`
	* 管理员账号: `admin`  密码: `123456`
	* 邮件发送: settings.py里，是测试账号，可自行修改
	* 支付宝keys: 是支付宝的沙箱环境
	* 修改admin界面为中文: `LANGUAGE_CODE = 'zh-hans'`
	* 修改为上海时间: `TIME_ZONE = 'Asia/Shanghai'`
	* 禁用utc时间: `USE_TZ = False`
	* 将apps和extra_apps目录加入path
	* 开发环境需要 `DEBUG = True` 以及 `ALLOWED_HOSTS = ['*']`
	* 开发环境收集静态文件: ./manage.py collectstatic 
	* STATIC_ROOT 和 STATICFILES_DIRS, DIRS里不能包含有ROOT，ROOT所指向的目录是 静态文件收集后的目录

## 问题相关 
	(很简单的django基础，相关代码里也都有注释) 感谢观看和star
	有任何问题欢迎提交Issue，或者发送邮箱 `binloveplay1314@qq.com`


## 目录说明：
* 学习阶段，项目架构和分层并没有划分的特别好。
* apps目录下放着相关app，例如goods, users
* extra_apps目录下放着相关外部apps，例如 xadmin
* db_tools存放着部分category_data，以及如何导入数据，商场所有数据均来自苏宁超市。里面有个小爬虫用于爬取各个分类下的商品信息
* media目录存放着后台上传的图片
* static目录存放着前台静态文件
* templates目录存放着模板文件

### 感谢观看 ---- > `展示页`。

----------

----------
![image](https://github.com/enjoy-binbin/binshop-Django/blob/master/img/1-index.png)
![image](https://github.com/enjoy-binbin/binshop-Django/blob/master/img/2-index.png)
![image](https://github.com/enjoy-binbin/binshop-Django/blob/master/img/3-category.png)
![image](https://github.com/enjoy-binbin/binshop-Django/blob/master/img/4-goodDetail.png)
![image](https://github.com/enjoy-binbin/binshop-Django/blob/master/img/5-login.png)
![image](https://github.com/enjoy-binbin/binshop-Django/blob/master/img/6-register.png)
![image](https://github.com/enjoy-binbin/binshop-Django/blob/master/img/7-fogetPWD.png)
![image](https://github.com/enjoy-binbin/binshop-Django/blob/master/img/8-cart.png)
![image](https://github.com/enjoy-binbin/binshop-Django/blob/master/img/9-order.png)
![image](https://github.com/enjoy-binbin/binshop-Django/blob/master/img/10-userinfo.png)
![image](https://github.com/enjoy-binbin/binshop-Django/blob/master/img/11-email.png)
![image](https://github.com/enjoy-binbin/binshop-Django/blob/master/img/12-address.png)
![image](https://github.com/enjoy-binbin/binshop-Django/blob/master/img/13-address.png)
![image](https://github.com/enjoy-binbin/binshop-Django/blob/master/img/14-orderList.png)
![image](https://github.com/enjoy-binbin/binshop-Django/blob/master/img/15-orderDetail.png)
----------

----------


## 编码过程中所做的一些笔记。

### 新建虚拟环境(这里用到的知识有 virtualenv,virtualenvwrapper)
	mkvirtualenv binshop
	workon binshop	

### 安装django，拥抱变化使用最新版
	pip install -i https://pypi.douban.com/simple django==2.1.3

### 依赖库的安装
	pip install -i https://pypi.douban.com/simple mysqlclient==1.3.10
	pip install Pillow


### 创建项目，也可以在Pycharm里创建
	django-admin startproject mysite

### 启动项目，visit http://127.0.0.1:8000
	python manage.py runserver 0:8000

* 为了让目录结构更好点，这里我分成了apps和extra_apps两个目录
* apps目录用来存放项目app, extra_apps里用来存放 xadmin这样外部app
* 在settings将这两个目录放入环境变量, 在pycharm中将两目录设为Source Root

		import sys
		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
		sys.path.insert(1, os.path.join(BASE_DIR, 'extra_apps'))


### settings里的设置
	# 数据库的设置
	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.mysql',
	        'NAME': 'binshop',
	        'USER': 'root',
	        'PASSWORD': '1123',
	        'HOST': '127.0.0.1'
	    }
	}

	LANGUAGE_CODE = 'zh-hans' # 修改admin界面为中文
	TIME_ZONE = 'Asia/Shanghai' # 修改为上海时间
	USE_TZ = False # 禁用utc时间

	STATIC_URL = '/static/'  # 静态文件目录
	STATICFILES_DIRS = (
	    os.path.join(BASE_DIR, 'static'),
	)
	
	MEDIA_URL = '/media/'  # 存储图片目录
	MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


### 启动admin
	settings里注册 admin
	python manage.py createsuper
 
	# 数据迁移，每次对model进行修改后都需要
	python manage.py makemigrations
	python manage.py migrate

	# 创建一个可以管理站点的用户
	python manage.py createsuperuser


### xadmin的安装:
	github地址：https://github.com/sshwsfc/xadmin
	根据xadmin里的依赖安装依赖库
	pip install httplib2 future django-crispy-forms django-formtools django-import-export
	注册xadmin,crispy_forms的app
	进行makemigrations和migrate和url配置，访问xadmin


### 数据库的设计
	django app的设计 和 各app models的设计
		users-用户管理
			UserProfile-用户信息
			EmailVerifyCode-邮箱验证码
			UserAddress-用户收货地址
	
		goods-商品管理
			GoodsCategory-商品分类
			Goods-商品信息
			GoodsImage-商品详情页里的轮播图 TODO
			Banner-首页轮播的商品

		trade-交易管理
			ShoppingCart-购物车
			OrderInfo-订单详情
			OrderGoods-订单里的商品详情 一对多

		user_operation-用户操作管理
			这里的views里存放着全局404和500的处理函数
		
		tools-工具箱
			alipay-支付宝网页版支付接口
			send_email-发送邮件的处理逻辑
			mixin_utils-mixin的小用法-Require登陆


### 扩展user表，django自带的auth_user表不能满足
	from django.contrib.auth.models import AbstractUser

	class UserProfile(AbstractUser):
	    """ 扩展原有的auth_user表 """
	    nickname = models.CharField(verbose_name=u'昵称', max_length=50, default='')
	    birthday = models.DateField(verbose_name=u'生日', null=True, blank=True)
	    gender = models.CharField(verbose_name=u'性别', max_length=6, choices=(('male', u'男'), ('female', u'女 ')), default='female')
	    address = models.CharField(verbose_name=u'地址', max_length=100, default='')
	    mobile = models.CharField(verbose_name=u'电话', max_length=11, null=True, blank=True)
	    image = models.ImageField(verbose_name=u'头像', max_length=100, upload_to='image/%Y/%m', default=u'image/default.jpg')
	
	    class Meta:
	        verbose_name = '用户信息'
	        verbose_name_plural = verbose_name
	
	    def __unicode__(self):
	        return self.username

	setting里设置和注册app
	AUTH_USER_MODEL = 'users.UserProfile'


### TemplateView用法
	from django.views.generic import TemplateView
	path('', TemplateView.as_view(template_name='index.html'), name='index'),


### 静态文件的引用
	{% load staticfiles %}
	{% static 'css/style.css' %}

### 前端取form的值
	{{ xx_form.data.key }}
	{{ xx_form.key.value }}
	
	{% if xx_form.errors.key %}{% endif %}
	{% for key, error in xx_form.errors.items %}error{%endfor%}

### django验证码插件（看g官网上的文档）
	Django Simple Captcha

	pip install django-simple-captcha==0.5.9
	add captcha to the INSTALLED_APPS in your settings
	run python manage.py migrate
	add an entry to your urls
	path('captcha/', include('captcha.urls'))


### 自定义商品图片上传路径
	# Models里
	def get_image_name(model, filename):
    	ext = os.path.splitext(filename)[-1]
    	return 'goods/images/{0}{1}'.format(model.name, ext)

	# models.Goods的字段里
		goods_front_image = models.ImageField(verbose_name="封面图", upload_to=get_image_name, null=True, blank=True,
		                                          default='goods/images/default.png')


### 调用django的ORM(db_tools有实践)
	import sys
	import os	
	
	pwd = os.path.dirname(os.path.realpath(__file__))
	sys.path.append(pwd+"../")
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "binshop.settings")
	
	import django
	django.setup()
	
	from goods.models import Goods
	
	goods = Goods.object.all()
	good = Goods()
	good.xxx = xxx
	good.save()


### Django重载authenticate
	class CustomBackend(ModelBackend):
	    """
	        settings里配置AUTHENTICATION_BACKENDS
	        这里将email和username和nickname都当作username进行Q并起来
	    """
	    def authenticate(self, request, username=None, password=None, **kwargs):
	        try:
	            user = UserProfile.objects.get(Q(username=username) | Q(nickname=username) | Q(email=username))
	            if user.check_password(password):
	                return user
	        except Exception as e:
	            return None
	
		settings添加
		AUTHENTICATION_BACKENDS = (
		    'users.views.CustomBackend',
		)


### 全局404和500设置，需要改成生产环境
	# 生产环境下配置404 500
	DEBUG = False
	ALLOWED_HOSTS = ['*']

	# 开发环境下可以在 urlpatterns后  分发media url
	urlpatterns后 + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

	### 下面两个参数， STATICFILES_DIRS 是一个存放 各个静态文件目录的元组， STATIC_ROOT是 在manage.py执行完collectstatic,所有你注册过的 APP 中所使用的静态文件均会收集到你所指定的 STATIC_ROOT 目录中，所以这两个目录不能一样
		STATIC_ROOT = os.path.join(BASE_DIR, 'static_collect')
		STATICFILES_DIRS = (
		    os.path.join(BASE_DIR, 'static'),
		)	

	# 生产环境用这个分发url， nginx的 TODO
	from django.views.static import serve  # 处理图片静态文件
	re_path('static/(?P<path>.*)', serve, {"document_root": STATIC_ROOT}),
	re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),

	# views里写的函数
		from django.shortcuts import render_to_response
		# 这里django2要加上 exception, django1.x就不用
		def page_not_found(request, exception):
		    """ 全局404处理函数 """
		    response = render_to_response('base/404.html', {})
		    response.code = 404
		    return response
		
		def page_error(request):
		    """ 全局500处理函数 """
		    res = render_to_response('base/500.html', {})
		    res.status_code = 500
		    return res

	# 404和500 在urls最后加上处理
		handler404 = 'user_operation.views.page_not_found'
		handler500 = 'user_operation.views.page_error'


### 用django-pure-pagination进行分页
	# 初始化
	pip install django-pure-pagination
	Add pure_pagination to INSTALLED_APPS

	# views
		try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(shops, 5, request=request)
        shops = p.page(page)

	# templates
		{% if shops.has_previous %}
			<li class="long"><a href="?{{ shops.previous_page_number.querystring }}">上一页</a></li>
        {% endif %}

        {% for page in shops.pages %}
            {% if page %}
                {% ifequal page shops.number %}
                    <li class="active"><a href="?{{ page.querystring }}">{{ page }}</a></li>
                {% else %}
                    <li><a href="?{{ page.querystring }}" class="page">{{ page }}</a></li>
                {% endifequal %}
            {% else %}
                <li class="none"><a href="">...</a></li>
            {% endif %}
        {% endfor %}

        {% if shops.has_next %}
            <li class="long"><a href="?{{ shops.next_page_number.querystring }}">下一页</a></li>
        {% endif %}


### 发送邮件
	注册了一个新浪微博
		binloveplay1314@sina.com
		sina1123.0
	在设置里 开启POP3/SMTP服务

	settings.py里的设置
		# 发送邮件的配置
		EMAIL_HOST = 'smtp.sina.com'
		EMAIL_PORT = 25
		EMAIL_HOST_USER = 'binloveplay1314@sina.com'
		EMAIL_HOST_PASSWORD = 'sina1123.0'
		EMAIL_USE_TLS = False  # 不使用TLS协议, 不https:443
		EMAIL_FROM = 'binloveplay1314@sina.com'  # 发件人

	实现：
		from random import Random
	
		from django.core.mail import send_mail
		
		from users.models import EmailVerifyCode
		from binshop.settings import EMAIL_FROM
		
		
		def send_email(email, type='register'):
		    """
		        发送邮件的方法
		        register:   注册账号
		        forget:     找回密码
		        change:     修改邮箱
		    """
		    email_code = EmailVerifyCode()
		    email_code.email = email
		    email_code.code = generate_random_str(16)
		    email_code.type = type
		    email_code.save()
		
		    # 发送邮件
		    if type == 'register':
		        subject = '彬彬商场注册激活链接'
		        message = '请点击下面的链接激活您的账号: http://xxx.xxx/active/{0}'.format(email_code)
		        status = send_mail(subject, message, EMAIL_FROM, [email])
		        if status:  # 发送成功
		            pass
		
		
		def generate_random_str(str_len=8):
		    """ 生成长度为str_len的随机字符串 """
		    str = ''
		    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
		    random = Random()
		    for i in range(str_len):
		        str += chars[random.randint(0, len(chars) - 1)]
		    return str


### python两种生成md5的方法
	# 使用md5包，py3已经移除
	import md5
	
	src = 'this is a md5 test.'   
	m1 = md5.new()   
	m1.update(src)   
	print m1.hexdigest()
	
	# 使用hashlib
	import hashlib   
	
	md5 = hashlib.md5()   
	md5.update(b'123')   
	print(md5.hexdigest())
	
	推荐使用第二种方法。