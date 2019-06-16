from django.urls import path, include
from sign import views_api

urlpatterns = [
    path('add_event/', views_api.add_event)
]