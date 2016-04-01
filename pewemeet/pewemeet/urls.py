"""pewemeet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from rencontre import views
from django.contrib.auth import views as auth_views
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.conf.urls import url


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.ListeProfile.as_view(), name="Profile_list"),
    #url(r'^profile/(?P<pk>\d+)$', views.LireProfile.as_view(), name='Profile_detail'),
    url(r'^new/', views.CreateProfile.as_view(), name='Profile_new'),
    #url(r'^login/', auth_views.login, {'template_name': 'rencontre/login.html' } ),
    url(r'^login/$', views.user_login, name='login'),
    #url(r'^logout/', auth_views.logout, {'template_name': 'rencontre/logout.html'}),
    url(r'^logout/$', views.user_logout, name='logout'),
   #url('^register/', CreateView.as_view(template_name='rencontre/register.html',form_class=UserCreationForm,success_url='/')),
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/(?P<pk>\d+)$',views.UserProfileDetail.as_view(),name='user_profile_detail'),
    #url(r'^profile/(?P<pk>\d+)/update/$', views.UserProfileUpdate.as_view(),name='rencontre/userprofile_form'),
    url(r'^profile/(?P<pk>\d+)/update/$', views.UpdateProfile.as_view(),name='Profile_update'),
    url(r'^listonight/$', views.ListeToNight.as_view(), name="tonight_list"),
    url(r'^listonight/(?P<pk>\d+)$',views.DetailToNight.as_view(),name='tonight_detail'),
    url(r'^message/$', views.message, name='message'),
    url(r'^search/(?P<pk>\d+)/$', views.SearchProfile.as_view(), name="SearchProfile"),
]


