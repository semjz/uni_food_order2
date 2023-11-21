from django.urls import path
from . import views

app_name = 'sms_service'

urlpatterns = [
    path("send/", views.broadcast_sms, name="send")
]