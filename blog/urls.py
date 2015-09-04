__author__ = 'PC'

import django_pydenticon.urls
from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', 'blog.views.home', name='home'),
    url(r'^page/(?P<page>[0-9]+)/$', 'blog.views.home', name='home'),
    url(r'^about$', 'blog.views.about', name='about'),
    url(r'^top$', 'blog.views.top', name='top'),
    url(r'^posts/(?P<post_id>[0-9]+)/$', 'blog.views.show_post', name='post'),
    url(r'^like_post/(?P<post_id>[0-9]+)/$', 'blog.views.like_post', name='like_post'),

    url(r'^create_post/$', 'blog.views.create_post', name='create_post'),
    url(r'^create_answer/$', 'blog.views.create_answer', name='create_answer'),

    url(r'^login$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^register$', 'blog.views.register', name='registration'),

    url(r'^follow/$', 'blog.views.follow', name='follow'),
    url(r'^unfollow/$', 'blog.views.follow', name='unfollow'),

    url(r'^users/(?P<user_name>[A-Za-z0-9_-]{3,30})/$', 'blog.views.show_profile', name='username_profile'),
    url(r'^users/(?P<user_name>[A-Za-z0-9_-]{3,30})/follows/$', 'blog.views.show_follows', name='userfollows'),
    url(r'^users/(?P<user_name>[A-Za-z0-9_-]{3,30})/followedby/$', 'blog.views.show_followedby', name='userfollowedby'),

    url(r'^identicon/', include(django_pydenticon.urls.get_patterns())),

]
