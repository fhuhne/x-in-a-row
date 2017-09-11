from django.conf.urls import url

from . import views

"""
Create URLs for the 3 views in views.py
"""
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^game/(?P<game_id>[0-9]+)/$', views.board, name='game'),
    url(r'^game/(?P<game_id>[0-9]+)/drop_tile/(?P<column>[0-9]+)/$', views.drop_tile, name='drop_tile'),
]
