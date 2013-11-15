from .dist import MIDDLEWARE_CLASSES, rel
MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + ('django_plop.middleware.PlopMiddleware',)
# will be created, defaults to /tmp/plop
PLOP_DIR = rel('data/plop') 
