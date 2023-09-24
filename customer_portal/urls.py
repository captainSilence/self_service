from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.getNewRequest, name='getData'),
    path('add/', views.addNewRequest)
]