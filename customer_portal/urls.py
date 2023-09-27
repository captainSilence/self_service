from django.urls import path
from . import views

urlpatterns = [ 
    path('new-request', views.NewRequest, name='newrequest'),
    path('new-request/<int:id>', views.NewRequestDetail),
]