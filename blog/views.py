import json
from math import ceil
import os
from django.conf import settings as djangoSettings
from django.core.exceptions import ValidationError
from django.core.files.images import ImageFile
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from blog.models import Post, UserForm, UserProfileForm, UserProfile, Like, PostForm

# Import the libraries.
import pydenticon
import hashlib

# Set-up a list of foreground colours (taken from Sigil).
from microblog import settings

foreground = [ "rgb(45,79,255)",
               "rgb(254,180,44)",
               "rgb(226,121,234)",
               "rgb(30,179,253)",
               "rgb(232,77,65)",
               "rgb(49,203,115)",
               "rgb(141,69,170)" ]

# Set-up a background colour (taken from Sigil).
background = "rgb(224,224,224)"

# Instantiate a generator that will create 5x5 block identicons using SHA1
# digest.
generator = pydenticon.Generator(5, 5, digest=hashlib.sha1,
                                 foreground=foreground, background=background)



def home(request, page=1):
    posts = []
    page = int(page)
    counter = 0
    if request.user.username:
        follows = request.user.userprofile.follows.all()
        all_posts = Post.objects.filter(Q(author__in=follows) | Q(author=request.user.userprofile)).all()
        counter = all_posts.count()
        posts = all_posts[(page-1)*20:page*20]
    context = {
        'posts': posts,
        'page': page,
        'max_page': ceil(counter/20),
    }
    return render(request, 'blog/main.html', context)


def about(request):
    return render(request, 'blog/about.html')


def show_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'blog/post.html', {'post': post})


def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                request.FILES['picture'].name = request.POST['username'] + os.path.splitext(request.FILES['picture'].name)[1]
                profile.picture = request.FILES['picture']
            else:
                resource = generator.generate(
                    request.POST['username'],
                    320,
                    320,
                    output_format="png",
                    padding=(10,10,10,10)
                )
                image = open(
                    os.path.join(djangoSettings.STATICFILES_DIRS[2], request.POST['username'] + str('.png')),
                    "wb")
                image.write(resource)
                image.close()
                profile.picture = os.path.join(djangoSettings.STATIC_URL, 'avatars', request.POST['username'] + str('.png'))


            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print(user_form.errors, profile_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'registration/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)


def show_profile(request, user_name):
    user = get_object_or_404(UserProfile, user__username=user_name)
    posts = Post.objects.filter(author__user__username=user_name).all()
    context = {
        'posts': posts,
        'user_id': user.id,
    }
    return render(request, 'blog/user_profile.html', context)


# Create post
def create_post(request, **kwargs):
    if request.method == 'POST':
        post_text = request.POST.get('text')
        response_data = {}

        if not post_text:
            raise ValidationError(
                ('Empty post'),
                code='invalid'
            )

        post = Post(text=post_text, author=request.user.userprofile)
        post.save()

        response_data['result'] = 'Create post successful!'
        response_data['postpk'] = post.id
        response_data['text'] = post.text
        response_data['created'] = post.pub_date.strftime('%b %d, %Y %I:%M %p')
        response_data['author'] = post.author.user.username
        response_data['author_link'] = str(reverse("username_profile", args=[post.author.user.username]))
        response_data['post_link'] = str(reverse("post", args=[post.id]))

        if request.POST.get('fullform'):
            print(request.FILES)
            if 'attachfile' in request.FILES:
                request.FILES['attachfile'].name = str(post.id) + '_' + str(request.user.username) + os.path.splitext(request.FILES['picture'].name)[1]
                post.attachfile = request.FILES['attachfile']
            post.save()
            return redirect('post', post_id=post.id)
        else:
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
    elif request.method == 'GET':
        text = request.GET.get('posttext')
        form = PostForm(initial={'text' : text})
        context = {
            'form' : form,
        }
        return render(request, 'blog/create_post.html', context)


# Create AJAX answer
def create_answer(request):
    if request.method == 'POST':
        post_text = request.POST.get('text')
        answerfor = Post.objects.get(id=request.POST.get('answerfor'))
        post = Post(text=post_text, answerfor=answerfor, author=request.user.userprofile)
        post.save()
        return redirect('post', post_id=post.id)

    else:
        post_id = request.GET.get('post_id')
        post = Post.objects.get(id=post_id)
        form = PostForm(initial={'answerfor' : post})
        return render(request, 'blog/answer.html', {'form': form})


# AJAX Like request
def like_post(request, post_id):
    method = request.POST.get('method')
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        if method == 'like':
            if Like.objects.filter(post=post, author=request.user.userprofile):
                raise ValidationError(
                    _('Invalid like: %(value)s'),
                    code='invalid',
                    params={'value': 'already exists'},
                )
            like = Like(author=request.user.userprofile, post=post)
            like.save()
        elif method == 'dislike':
            like = Like.objects.get(author=request.user.userprofile, post=post)
            like.delete()

        post.save()
        post.author.save()
        request.user.userprofile.save()

        response_data = {}
        response_data['post_id'] = post.id
        response_data['likes'] = post.like_set.count()
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def show_follows(request, user_name):
    user = UserProfile.objects.get(user__username=user_name)
    follows = user.follows.all()
    context = {
        'title': 'Followed by',
        'follows': follows,
        'user_id': user.id,
        'user_name': user_name,
    }
    return render(request, 'blog/show_follows.html', context)


def show_followedby(request, user_name):
    user = UserProfile.objects.get(user__username=user_name)
    followedby = UserProfile.objects.filter(follows=user)
    context = {
        'title': 'Followers of',
        'follows': followedby,
        'user_id': user.id,
        'user_name': user_name,
    }
    return render(request, 'blog/show_follows.html', context)


def top(request):
    return render(request, 'blog/top.html')


def follow(request):
    if request.method == 'POST':
        method = request.POST.get('method')
        user_id = request.POST.get('user_id')
        followto = UserProfile.objects.get(id=user_id)
        if method == 'follow':
            request.user.userprofile.follows.add(followto)
        else:
            request.user.userprofile.follows.remove(followto)
        return HttpResponse(
            'OK', content_type='text/plain'
        )
    elif request.method == 'GET':
        return HttpResponse(
            'Not OK', content_type='text/plain'
        )