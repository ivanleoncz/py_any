from django.urls import path

from .views import CetesView

urlpatterns = [
    path('cetes/', CetesView.as_view())
]