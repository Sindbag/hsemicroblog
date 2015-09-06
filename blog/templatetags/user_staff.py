__author__ = 'PC'
from django.core.urlresolvers import reverse
from django import template
from blog.models import Post, UserProfile, Like

register = template.Library()

@register.inclusion_tag("blog/miniprof.html")
def user_profile_mini(user_id):
    user = UserProfile.objects.get(id=user_id)
    return {'user': user,
            }

@register.simple_tag
def follow(user_id, follow_id):
    if user_id == follow_id:
        return ''
    user = UserProfile.objects.get(id=user_id)
    if user.follows.filter(id=follow_id):
        return '<button type="button" class="close" aria-label="Unfollow"><span class="follow-button" aria-hidden="true">&times;</span></button>'
    else:
        return '<span class="glyphicon glyphicon-plus follow-button" aria-hidden="true"></span>'

@register.simple_tag
def userpic_src(user_id):
    user = UserProfile.objects.get(id=user_id)
    if user.picture:
        return user.picture
    else:
        return reverse("django_pydenticon:image",
                            kwargs={"data": user})

@register.inclusion_tag("blog/showpost.html", takes_context=True)
def show_post(context, post, depth):
    return {'post': post,
            'depth': depth-1,
            'user': context['user'],
            }

@register.simple_tag
def pagination(page, pages):
    stack = set()
    page = int(page)
    pages = int(pages)
    if pages > 2:
        stack.update([1, 2, 3, pages, page, pages-1, pages-2])
    elif pages == 2:
        stack.update([1, 2])
    text = ''
    if len(stack):
        text = '<nav><ul class="pagination">'
        for i in sorted(stack):
            pageclass = ''
            if page == i:
                pageclass = 'active'
            text += '<li class="' + pageclass +'"><a href="'+reverse('home', kwargs={"page" : str(i)})+'">'+str(i)+'</a></li>'
        text += '</ul></nav>'
    return text

@register.simple_tag
def follow(user, username):
    user = UserProfile.objects.get(user__username=user)
    author = UserProfile.objects.get(user__username=username)
    if user == author:
        return ''
    if author in user.follows.all():
        return '<a class="unfollowman" data-id="' + str(author.id) + '"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span></a>'
    else:
        return '<a class="followman" data-id="' + str(author.id) + '"><span class="glyphicon glyphicon-check" aria-hidden="true"></span></a>'

@register.simple_tag
def like_post(user_name, post_id):
    if (user_name != 'AnonymousUser'):
        user = UserProfile.objects.get(user__username=user_name)
    else:
        user = ''
    post = Post.objects.get(id=post_id)
    picture = 'glyphicon glyphicon-thumbs-up'
    opacity = 'disliked'
    method = 'like_button'
    likes = post.likes
    if user:
        if post.author == user:
            return '<div class="likepoint" data-id="' + str(post.id) + '"><span class="post_likes">' + str(likes) + '&nbsp;</span><span class="likepic liked ' + picture + '" aria-hidden="true"></span></div>'
        elif Like.objects.filter(author=user, post=post):
            # picture = 'glyphicon glyphicon-thumbs-down'
            opacity = 'liked'
            method = 'dislike_button'

    return '<div class="likepoint" data-id="' + str(post.id) + '"><span class="post_likes">' + str(likes) + '&nbsp;</span>' + \
           '<a class="liker ' + method + '"><span class="likepic ' + opacity + ' ' + picture + '" aria-hidden="true"></span></a>' + \
                                                                                         '</div>'