from settings import *

DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = ['http://ec2-54-148-68-112.us-west-2.compute.amazonaws.com/', 'localhost']
STATIC_ROOT = os.path.join(BASE_DIR, 'static')