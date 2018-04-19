from django.contrib import admin

from django.conf.urls import include, url

from django.contrib.auth import views as auth_views
from rides_handling import views as rides_handling_views

urlpatterns = [
    url(r'admin/', admin.site.urls),

    url(r'^$', rides_handling_views.home, name='home'),
    url(r'^login/$', rides_handling_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', rides_handling_views.signup, name='signup'),
]
