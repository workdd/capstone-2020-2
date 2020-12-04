import sys

sys.path.append('../')

from celery import Celery
from celery.utils.log import get_task_logger

celery_logger = get_task_logger('tasks')

celery = Celery('tasks', broker='redis://localhost:6379', backend='redis://localhost:6379')
# celery.conf.CELERYD_CONCURRENCY = 4
celery.conf.CELERY_IMPORTS=("api.tasks")


# def make_celery(app): # Celery 객체를 만들어 반환하는 함수, Flask 인스턴스 객체를 인자로 받음
#     celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
#     celery.conf.update(app.config) # Flask 인스턴스 객체는 Celery 초기화 설정을 전달하고 Celery가 Flask 인됨없이 독립적으로 실행됨을 보장하기 위해 사용
#     TaskBase = celery.Task
#
#     class ContextTask(TaskBase): # Celery가 작업(Task)를 수행하기 위해 사용되는 기본 클래스, celery의 Task를 상속
#         abstract = True # ContrstTask 클래스가 추상화 클래스로서 Celery가 수행해야 할 작업을 인식하지 않게 하기 위해서 사용
#
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return TaskBase.__call__(self, *args, **kwargs)
#     celery.Task = ContextTask # Context 클래스를 Celery 객체의 Task가 참조하도록 설정
#     return celery
#
# celery_logger = get_task_logger('app')
# celery = make_celery(app)  # Celery 객체 생성