# импортировать celery
from myshop.celery import app as celery_app 

__all__ = ['celery_app']