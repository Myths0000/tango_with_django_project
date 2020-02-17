"""
    path() function:
    1. empty string '' means nothing after the host address
    2. second parameter: what view to call
    3. third parameter (optional): a way to reference the view
"""

from django.urls import path
from rango import views

app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),
]
