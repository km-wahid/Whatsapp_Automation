from django.urls import path
from .views import  send_message_api

urlpatterns = [
    
    path('api/', send_message_api, name='send_message_api'),
   
   
]
