# 大四毕业设计课题

#### 系统主要是针对实现了对网上超市购物的自动化管理，它使得商品的管理工作走向全面自动化、规范化，且通过网络廉价快捷的通讯手段，消除时间与空间带来的障碍，从而大大的节约了交易成本，扩大了交易范围。构件一个网络购物系统能让我们更适应当今社会快节奏生活，使得顾客足不出户便可以方便轻松地选购自己喜欢的商品。
#### 系统主要是为用户提供网上注册、网上浏览商品信息、网上购物的功能以及商家后台管理：包括添加商品、删除商品和修改商品等重要功能，这些功能，极大地提高了购物的效率。
#### 开发一套网上商城购物系统,包括了用户账号管理、用户信息管理、超市商品管理、超市后台管理、添加商品信息、修改商品信息、删除商品信息、用户注册，用户查看商品信息、用户购买商品、等重要的功能。系统逐步展开设计，包括系统分析，系统总体设计，系统的详细设计等，最后对系统进行全面的测试。


# 开发环境:  先简单的来，前后端不分离。
	win10 x86，python3.6，django2.1.3，时间 18年12月


# 新建虚拟环境(这里用到的知识有 virtualenv,virtualenvwrapper)
	mkvirtualenv binshop
	workon binshop	

# 安装django，拥抱变化使用最新版
	pip install -i https://pypi.douban.com/simple django==2.1.3

# 依赖库的安装
	pip install -i https://pypi.douban.com/simple mysqlclient==1.3.10
	pip install Pillow


# 创建项目，也可以在Pycharm里创建
	django-admin startproject mysite

# 启动项目，visit http://127.0.0.1:8000
	python manage.py runserver 0:8000

# 为了让目录结构更好点，这里我分成了apps和extra_apps两个目录
# apps目录用来存放项目app, extra_apps里用来存放 xadmin这样外部app
# 在settings将这两个目录放入环境变量, 在pycharm中将两目录设为Source Root
	import sys
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
	sys.path.insert(1, os.path.join(BASE_DIR, 'extra_apps'))


# settings里的设置
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


# 启动admin
	settings里注册 admin
	python manage.py createsuper

# 数据迁移，每次对model进行修改后都需要
	python manage.py makemigrations
	python manage.py migrate

# 创建一个可以管理站点的用户
	python manage.py createsuperuser


# xadmin的安装:
	github地址：https://github.com/sshwsfc/xadmin
	根据xadmin里的依赖安装依赖库
	pip install httplib2 future django-crispy-forms django-formtools django-import-export
	注册xadmin,crispy_forms的app
	进行makemigrations和migrate和url配置，访问xadmin

# 数据库的设计

django app的设计 和 各app models的设计
	users-用户管理
		users.UserProfile-用户信息
		users.EmailVerifyCode-邮箱验证码

	goods-商品管理		




# 扩展user表，django自带的auth_user表不能满足
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






# TemplateView用法
	from django.views.generic import TemplateView
	path('', TemplateView.as_view(template_name='index.html'), name='index'),





# 静态文件的引用
	{% load staticfiles %}
	{% static 'css/style.css' %}


# Users.Views
	class LoginView(View):
	    """ 基于类的用法 """
	    def get(self, request):
	        return render(request, 'login.html', {})
	
	    def post(self, request):
	        login_form = LoginForm(request.POST)
	        if login_form.is_valid():
	            username = request.POST.get('username', '')
	            password = request.POST.get('password', '')
	            user = authenticate(username=username, password=password)
	            if user is not None:
	                login(request, user)
	                return render(request, 'index.html', {})
	            else:
	                # TODO: 账号错误 或 密码错误
	                return render(request, 'login.html',{'msg': '账号或密码错误'})
	        else:
	            return render(request, 'login.html', {'login_form': login_form})


	from django import forms
	class LoginForm(forms.Form):
	    """ Login的Form对前台登陆页面进行验证 """
	    username = forms.CharField(required=True)
	    password = forms.CharField(required=True, min_length=2)


# django验证码插件
	Django Simple Captcha

	pip install django-simple-captcha==0.5.9
	add captcha to the INSTALLED_APPS in your settings
	run python manage.py migrate
	add an entry to your urls
		path('captcha/', include('captcha.urls'))



