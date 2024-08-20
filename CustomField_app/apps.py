from django.apps import AppConfig


class CustomfieldAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CustomField_app'
