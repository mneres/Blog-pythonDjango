from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.home),

    url(r'^post/mypost/$', views.list_my_post, name="list_my_post"),
    url(r'^post/listByTag/(?P<tag>[^/]+)/$', views.post_list_by_tag, name="list_post_by_tag"),
    url(r'^post/search/$', views.post_search, name="post_search"),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/remove/$', views.post_remove, name='post_remove'),
    url(r'^post/(?P<pk>[0-9]+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),

    url(r'^post/import/$', views.import_post, name='import_post'),
    url(r'^post/import/load$', views.soup_load_post, name='soup_load_post'),

    url(r'^post/(?P<pk>[0-9]+)/tag/$', views.import_post_add_tag, name='import_post_add_tag'),
    url(r'^post/(?P<pk>[0-9]+)/add/tag$', views.post_add_tag, name='post_add_tag'),

    url(r'^comment/(?P<pk>[0-9]+)/remove/$', views.comment_remove, name='comment_remove'),

    url(r'^user/add/$', views.add_user, name='add_user')
]