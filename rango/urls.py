"""
    path() function:
    1. empty string '' means nothing after the host address
    2. second parameter: what view to call
    3. third parameter (optional): a way to reference the view
"""

from django.urls import path
from django.urls import include
from rango import views

app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
]
