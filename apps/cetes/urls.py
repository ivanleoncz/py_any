from django.urls import path

from . import views

urlpatterns = [
    path('cetes/', views.index, name='index')
]