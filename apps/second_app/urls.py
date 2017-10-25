
from django.conf.urls import url
from . import views
from ..login_app.models import User

urlpatterns = [
    url(r'^dashboard$', views.dashboard),
    url(r'^profile/(?P<id>\d+)$', views.profile),
    url(r'^addFriend/(?P<id>\d+)$', views.addFriend),
    url(r'^edit/(?P<id>\d+)$', views.edit),
    url(r'^update/(?P<id>\d+)$', views.update),
    url(r'^delete/(?P<id>\d+)$', views.delete),
]