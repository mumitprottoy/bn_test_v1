from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered

app_models = apps.get_app_config(__name__.split('.')[-2]).get_models()

for model in app_models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
