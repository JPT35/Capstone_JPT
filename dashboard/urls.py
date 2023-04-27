from django.urls import path

from . import views 

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='index'), # can be left empty because dashbord url is located in greenCRM url file
]