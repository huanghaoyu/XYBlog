from django.conf.urls import url
from . import views

app_name = 'blog'
urlpatterns = [
    # ex: /blog/
    url(r'^$', views.index, name='index'),
    # ex: /blog/list/
    url(r'^list/$', views.list, name='list'),
    # ex: /blog/5/
    url(r'^detail/(?P<blog_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /blog/register/
    url(r'^register/$', views.register, name='register'),
    # ex: /blog/login/
    url(r'^login/$', views.login, name='login'),
    # ex: /blog/write/
    url(r'^write/$', views.write, name='write'),
    # ex: /blog/logout/
    url(r'^logout/$', views.logout, name='logout'),
]
