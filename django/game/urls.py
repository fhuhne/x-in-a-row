from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^game/(?P<game_id>[0-9]+)/$', views.board, name='game'),
    url(r'^game/(?P<game_id>[0-9]+)/drop_tile/(?P<column>[0-9]+)/$', views.drop_tile, name='drop_tile'),
]
