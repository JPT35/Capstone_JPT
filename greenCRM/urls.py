from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views
from django.urls import path, include

from core.views import index, about
from userprofile.forms import LoginForm


urlpatterns = [
    path('', index, name='index'),
    path('dashboard/leads/', include ('lead.urls')), # configuring all urls beginning with dashboard/leads
    path('dashboard/clients/', include('client.urls')),
    path('dashboard/', include('dashboard.urls')), # setting all urls that begin with dashbord to use dashboard.urls file
    path('dashboard/teams/', include('team.urls')),
    path('dashboard/report/', include ('report.urls')),
    path('dashboard/', include('userprofile.urls')),
    path('about/', about, name='about'),
    path('log-in/', views.LoginView.as_view(template_name='userprofile/login.html', authentication_form=LoginForm), name='login'),
    path('log-out/', views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
