from django.urls import path
from web.views import *
urlpatterns = [
    path('upload/', upload_csv, name='upload_csv'),
    
    path('sent/', send_whatsapp_message, name='send_whatsapp_message'),
    path('template/', create_template, name='create_template'),
    path('campaign_view/', campaign_view, name='campaign_view'),
    path('create_whatsapp_session/', create_whatsapp_session, name='create_whatsapp_session'),
    path('dashboard', dashboard, name='dashboard'),
    path('user_list/', user_list, name='user_list'),
    path('history/', history, name='history'),
    path('api_docs/', api_docs, name='api_docs'),
    path('', login_view, name='login_view'),
    path('logout', logout_view, name='logout_view'),
    path('login_qr', login_qr, name='login_qr'),
    # path('input_number/', input_number, name='input_number'),
    path("qr-json", proxy_qr_json, name="proxy_qr_json"),
   


]
