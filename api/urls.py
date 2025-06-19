from django.urls import path
from . import views

urlpatterns = [
    path('pro-login/', views.ProLoginAPI.as_view(), name='pro-login'),
]