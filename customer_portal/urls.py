from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [ 
    path('new-request', views.NewRequest.as_view(), name='newrequest'),
    path('new-request/<int:id>', views.NewRequestDetail.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)