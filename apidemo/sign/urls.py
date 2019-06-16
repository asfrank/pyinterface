from django.urls import path, include
from sign import views_api

urlpatterns = [
    path('add_event/', views_api.add_event),
    path('get_event_list', views_api.get_event_list),
    path('user_sign', views_api.user_sign),
]