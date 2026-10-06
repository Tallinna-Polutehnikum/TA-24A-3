from django.urls import path

from . import views

app_name = 'cinema'

urlpatterns = [
    path('', views.health, name='health'),
]
