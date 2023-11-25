from django.apps import AppConfig


"""class UsersConfig(AppConfig):
    name = 'users'
"""
class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'