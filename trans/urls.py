from django.urls import path
from . import views

app_name = 'trans'
urlpatterns = [
    path('trans/', views.index, name='index'),
]