# coding:utf-8
import os

# JWT加密，以及salt盐
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'omD4PtIjczXouDCqaiHgh2yhSQMcUwdPZyPXUClJ5ig2H2blaWyW4X0GoMeKxSPf')
JWT_ALG = os.environ.get('JWT_ALG', 'HS256')
JWT_SALT = os.environ.get('JWT_SALT', 'mysalt')
COOKIE_NAME = os.environ.get('COOKIE_NAME', 'my_cookie')

# ===============================================================================
# debug toolbar 配置
# ===============================================================================
DEBUG_TOOLBAR_PATCH_SETTINGS = False
DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': "http://code.jquery.com/jquery-2.1.1.min.js"
}

# 内网ip列表
INTERNAL_IPS = ['127.0.0.1']

# ==============================================================================
# 中间件和应用
# ==============================================================================
# 自定义中间件
MIDDLEWARE_CLASSES_CUSTOM = [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware'
]

# 自定义APP
INSTALLED_APPS_CUSTOM = [
    # add your app here...
    # Note: 请注意在第一次syncdb时不加自己的app
    # 'debug_toolbar',
    'user'
]

# ===============================================================================
# 数据库设置
# ===============================================================================

DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
DB_PORT = os.environ.get('DB_PORT', '3306')
DB_NAME = os.environ.get('DB_NAME', 'test_user')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PWD = os.environ.get('DB_PWD', 'mypwd')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PWD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    },
}

# ===============================================================================
# 日志级别
# ===============================================================================
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG')
