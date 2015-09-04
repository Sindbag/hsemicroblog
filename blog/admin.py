from django.contrib import admin
from blog.models import Post, UserProfile, Like

admin.site.register([Post, UserProfile, Like])