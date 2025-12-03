"""
Asgi configuracion per al projecte medflow.
esta expone el callable ASGI com una variable a nivell de mòdul anomenada ``application``.
    
para mas información sobre este archivo, vea
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medflow.settings')

application = get_asgi_application()
