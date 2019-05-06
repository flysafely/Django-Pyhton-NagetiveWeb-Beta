"""
Django settings for nagetiveSite project.

Generated by 'django-admin startproject' using Django 2.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$@&+60oqu5u900a+1*qo*!5nn#ljd3lj=3%p@#dmw%=mle$+_x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'www.nagetive.com', 'www.nagetives.com', '192.168.3.69','192.168.3.79']

APP_NAMES = ['NTWebsite', ]
# Application definition

INSTALLED_APPS = [
    #'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # 使用了staticfiles 就必须定义STATIC_URL   URL路由指向STATIC_ROOT路径
    'django.contrib.staticfiles',
    'NTWebsite',
    'ckeditor',
    'ckeditor_uploader',
    'CustomFunctions',
    'imagekit',
    'xadmin',
    'crispy_forms',
    'reversion',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'NTConfig.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 默认路径直接找文件夹名称为templates的，如果有这个名称的文件夹就不用单独设定，其他特定名称的路径需要在DIR中设置
        'DIRS': [os.path.join(BASE_DIR, APP_NAMES[0], 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "django.template.context_processors.media",
                "django.template.context_processors.static",
            ],
        },
    },
]


CACHES = {
    "default": {  # 连接池名称
        # 以下是连接池的相关配置
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:1101",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
            "PASSWORD": "q63785095",
        }
    },
    "flysafely": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:1101",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
            "PASSWORD": "q63785095",
        }
    },
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'  # 引擎
SESSION_CACHE_ALIAS = 'default'

WSGI_APPLICATION = 'NTConfig.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
AUTH_USER_MODEL = '.'.join((APP_NAMES[0], 'User'))

LANGUAGE_CODE = 'zh-Hans'

FILE_CHARSET = 'utf-8'

DEFAULT_CHARSET = 'utf-8'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#LOGIN_URL = '/login/'

# 当在开发模式下时候 URL映射有效 
# 作用是告诉请求，在服务器的那个物理位置去获取资源
# 例如 请求链接中出现127.0.0.1:8000/static/   就会自动首先在DIRS中寻找资源，再到App static中寻找
# 当找到第一个符合的资源时候就会停止搜索

# 当处于部署模式时候，即DEBUG=False，STATIC_URL物理位置映射失效，在不开启web服务器的静态资源位置映射的情况下，
# URL中即使出现http:127.0.0.1:8000/static/***，服务器也不知道从什么物理位置获取资源
STATIC_URL = '/static/'

# 当执行python manage.py collectstatic 时候会将DIRS中目录下的文件也收集到STATIC_ROOT当中
# 会将os.path.join(BASE_DIR, "abc")路径中的文件，打包成名字为test的文件夹收集到STATIC_ROOT当中
# 如果os.path.join(BASE_DIR,
# "abc")不存在会报错，路径跟STATIC_ROOT一样也会报错，因为即将收集的文件路径跟即将存放的文件路径一样，
# 不指定该路径，django无法从APP内找到资源，原因未知
STATICFILES_DIRS = [os.path.join(BASE_DIR, APP_NAMES[0], "static/"), ]

# python manage.py collectstatic 执行后的存放目录
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
APP_ROOT = os.path.join(BASE_DIR)

# 用于存放用户上传资源
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
CKEDITOR_UPLOAD_PATH = "TopicPicUpload/" # Ckeditor文件上传目录是MEDIA_ROOT + CKEDITOR_UPLOAD_PATH 组合而成，是简单的字符串拼接，不是os.path.join自动补全斜杆，所以需要在
'''
STATICFILES_DIRS = (
    ('css', os.path.join(STATIC_ROOT, 'css/')),
    ('js', os.path.join(STATIC_ROOT, 'js/')),
    ('images', os.path.join(MEDIA_ROOT, 'images/')),
    ('upload', os.path.join(MEDIA_ROOT, 'upload/')),
)
'''


# DEBUG = True 开发环境中的时候
# Django接管相关url的路径指向第一DIRS，第二App内static
# STATIC_URL 映射有效
# STATICFILES_DIRS 指定有效，作用为：先在STATICFILES_DIRS指定路径中寻找资源，如果没有再到App 中static寻找资源


# DEBUG = False 部署环境中的时候
# django.contrib.staticfiles 功能失效
# 由web服务器接管URL路由功能，例如Nginx 的路径指定设置location /{}
# STATIC_URL 映射无效，Web服务器直接接管
# STATICFILES_DIRS 指定无效，Web服务器直接接管




# 增加ckeditor的功能
CKEDITOR_CONFIGS = {
    'admin': {
        'toolbar': (
            ['div', 'Source', '-', 'Save', 'NewPage', 'Preview', '-', 'Templates'],
            ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord',
                '-', 'Print', 'SpellChecker', 'Scayt'],
            ['Undo', 'Redo', '-', 'Find', 'Replace',
             '-', 'SelectAll', 'RemoveFormat'],
            ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea',
             'Select', 'Button', 'ImageButton', 'HiddenField'],
            ['Bold', 'Italic', 'Underline', 'Strike',
             '-', 'Subscript', 'Superscript'],
            ['NumberedList', 'BulletedList', '-',
             'Outdent', 'Indent', 'Blockquote'],
            ['JustifyLeft', 'JustifyCenter',
                            'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Flash', 'Table', 'HorizontalRule',
             'Smiley', 'SpecialChar', 'PageBreak'],
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['Maximize', 'ShowBlocks', '-', 'About', 'pbckcode'],
        ),
    },
    'html': {
        'toolbar': (
            ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord',
                '-', 'Print', 'SpellChecker', 'Scayt'],
            ['Undo', 'Redo', '-', 'Find', 'Replace',
             '-', 'SelectAll', 'RemoveFormat'],
            ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea',
             'Select', 'Button', 'ImageButton', 'HiddenField'],
            ['Bold', 'Italic', 'Underline', 'Strike',
             '-', 'Subscript', 'Superscript'],
            ['NumberedList', 'BulletedList', '-',
             'Outdent', 'Indent', 'Blockquote'],
            ['JustifyLeft', 'JustifyCenter',
                            'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink', 'Anchor'],
            ['Table', 'HorizontalRule',
             'Smiley', 'SpecialChar', 'PageBreak'],
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['Maximize', 'ShowBlocks', '-', 'About', 'pbckcode'],
        ),
    }
}

'''
    'html': {
        'toolbar': (
            ['div', 'Source', '-', 'Save', 'NewPage', 'Preview', '-', 'Templates'],
            ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord',
                '-', 'Print', 'SpellChecker', 'Scayt'],
            ['Undo', 'Redo', '-', 'Find', 'Replace',
             '-', 'SelectAll', 'RemoveFormat'],
            ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea',
             'Select', 'Button', 'ImageButton', 'HiddenField'],
            ['Bold', 'Italic', 'Underline', 'Strike',
             '-', 'Subscript', 'Superscript'],
            ['NumberedList', 'BulletedList', '-',
             'Outdent', 'Indent', 'Blockquote'],
            ['JustifyLeft', 'JustifyCenter',
                            'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink', 'Anchor'],
            ['Table', 'HorizontalRule',
             'Smiley', 'SpecialChar', 'PageBreak'],
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['Maximize', 'ShowBlocks', '-', 'About', 'pbckcode'],
        ),
    }

'''

JoinStringMap = {'Comment': {'JoinStr': '评论了',
                             'QueryString': 'TopicInfo.objects.get(ObjectID=%s)'},
                 'CommentReplay': {'JoinStr': '回复了',
                                   'QueryString': 'CommentInfo.objects.get(ID=%s)'},
                 'Topic1': {'JoinStr': '赞了',
                            'QueryString': 'TopicInfo.objects.get(ObjectID=%s)'},
                 'Topic0': {'JoinStr': '怼了',
                            'QueryString': 'TopicInfo.objects.get(ObjectID=%s)'},
                 'Comment1': {'JoinStr': '赞了',
                              'QueryString': 'TopicInfo.objects.get(ObjectID=%s)'},
                 'Comment0': {'JoinStr': '怼了',
                              'QueryString': 'TopicInfo.objects.get(ObjectID=%s)'}, }


if __name__ == '__main__':
    print(os.path.join(BASE_DIR, APP_NAMES[0]))
