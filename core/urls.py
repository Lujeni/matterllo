# -*- coding: utf-8 -*-
from django.conf.urls import url

from core.views import (
    BoardView, BoardDetailView, WebhookDetailView, WebhookCreateView, BridgeCreateView,
    BridgeDetailView, BridgeListView, MatterlloWizard, TrelloCallbacksView, OauthView, TokenView
)


urlpatterns = [
    url(r'^$', OauthView.as_view(), name='index'),

    url(r'^callback/(?P<board_id>[0-9]+)/$', TrelloCallbacksView.as_view(), name='callback'),
    url(r'^accessToken/',TokenView.as_view(), name='access_token'),

    url(r'^board/$', BoardView.as_view(), name='board'),
    url(r'^board/(?P<pk>[0-9]+)/$', BoardDetailView.as_view(), name='board_detail'),

    url(r'^webhook/(?P<pk>[-\w]+)/$', WebhookDetailView.as_view(), name='webhook_detail'),
    url(r'^webhook/add/(?P<board_id>[0-9]+)/', WebhookCreateView.as_view(), name='webhook_create'),

    url(r'^bridge/(?P<pk>[-\w]+)/$', BridgeDetailView.as_view(), name='bridge_detail'),
    url(r'^bridges/$', BridgeListView.as_view(), name='bridge_list'),
    url(r'^bridge/add/(?P<board_id>[0-9]+)/(?P<webhook_id>[0-9]+)/', BridgeCreateView.as_view(), name='bridge_create'),
]
