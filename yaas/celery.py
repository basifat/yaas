# from __future__ import absolute_import

# import os

# from celery import Celery

# # set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yaas.settings')

# from django.conf import settings  # noqa

# app = Celery('yaas')

# # Using a string here means the worker will not have to
# # pickle the object when using Windows.
# app.config_from_object('django.conf:settings')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))
'''
# from __future__ import absolute_import

# import os

# from celery import Celery

# # set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yaas.settings')

# from django.conf import settings  # noqa

# app = Celery('yaas')

# # Using a string here means the worker will not have to
# # pickle the object when using Windows.
# app.config_from_object('django.conf:settings')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))
    '''

from __future__ import absolute_import

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yaas.settings')

from django.conf import settings

#old version
# app = Celery('yaas',
#              broker='amqp://',
#              backend='amqp://',
#              include=['yaas.tasks'])

app = Celery('yaas')

# Optional configuration, see the application user guide.

app.config_from_object('django.conf:settings')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

#old version
# app.conf.update(
#     CELERY_TASK_RESULT_EXPIRES=3600,
# )

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

# if __name__ == '__main__':
#     app.start()