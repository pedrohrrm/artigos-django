
from django.urls import path
from . import views
from .views import chatbot_response

urlpatterns = [
    path('', views.home ,name='home'),
    path('chatbot-response/', chatbot_response, name='chatbot-response'),

]
