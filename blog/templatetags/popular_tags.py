from django.db.models import Count, Sum

__author__ = 'PC'
from django import template
from blog.models import Post, UserProfile, Like
from datetime import datetime, timedelta

register = template.Library()

# N most popular posts ordered by likes published in last M days
@register.inclusion_tag("blog/popular.html", takes_context=True)
def popular_posts(context, count, days):
    #pop_posts = Post.objects.filter(pub_date__gte=datetime.now()-timedelta(days=days)).order_by('-likes')[:count]
    pop_posts = Post.objects.order_by('-likes')[:count]
    return {'compilation': pop_posts,
            'text': 'likes',
            'count': count,
            'username': str(context['user']),
            }

# N most popular users ordered by likes for all time
@register.inclusion_tag("blog/popular_people.html", takes_context=True)
def popularities(context, count):
    pop_people = UserProfile.objects.annotate(likes=Count('post__likes')).order_by('-likes')[:count]
    return {'compilation': pop_people,
            'text': 'likes',
            'count': count,
            'username': context['user'],
            }