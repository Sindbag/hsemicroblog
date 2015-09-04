import os
from django import forms
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.db.models import Sum

from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.core.files import File
import urllib.request
import datetime


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # User follows other users
    follows = models.ManyToManyField('self', symmetrical=False, blank=True, related_name="followers")

    # The additional attributes
    website = models.URLField(blank=True)
    picture = models.ImageField(
        upload_to='static/avatars',
        blank=True,
        default=None
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    likes = models.PositiveIntegerField(default=0)

    # Update Likes count
    def save(self, *args, **kwargs):
        # Update likes
        self.likes = Like.objects.filter(post__author=self).count()
        # self.follows.add(UserProfile.objects.get(id=self.id))
        super(UserProfile, self).save(*args, **kwargs)

    def posts_count(self):
        return Post.objects.filter(author__id=self.id).count()

    def follows_c(self):
        return self.follows.count()

    def follows_people(self, count=5):
        return self.follows.all()[:count]

    def followed_by_c(self):
        return UserProfile.objects.filter(follows=self).count()

    def followed_by(self, count=5):
        return UserProfile.objects.filter(follows=self).all()[:count]

    # Override the __str__() method to return out something meaningful!
    def __str__(self):
        return self.user.username


"""
# Hashtags for future, todo: popularity sort
class Hashtags(models.Model):
    text = models.CharField(max_length=100)
    posts = models.ManyToManyField(Post, blank=True)
"""


class Post(models.Model):
    # Date, text and author
    text = models.TextField(max_length=280, help_text="What's new?")
    author = models.ForeignKey(UserProfile)
    pub_date = models.DateTimeField('publication date', default=timezone.now)

    # If the post is answer
    answerfor = models.OneToOneField('self', blank=True, null=True)

    # Likes counter
    likes = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        # Update likes
        self.likes = Like.objects.filter(post__id=self.id).count()
        super(Post, self).save(*args, **kwargs)

    def likes_count(self):
        self.likes = Like.objects.filter(post__id=self.id).count()
        return self.likes

    # Display in admin panel
    def __str__(self):
        return self.text[:80] + ' | ' + self.author.user.username

    def answers(self):
        return Post.objects.filter(answerfor=self.id).all()

    def answers_c(self):
        return Post.objects.filter(answerfor=self.id).count()

    class Meta:
        get_latest_by = "pub_date"
        ordering = ['-pub_date']


# Likes
class Like(models.Model):
    author = models.ForeignKey(UserProfile)
    post = models.ForeignKey(Post)
    pub_date = models.DateTimeField('like_date', default=timezone.now)

    def __str__(self):
        return self.author.user.username + ' liked post #' + str(self.post.id)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # exclude = ['author', 'updated', 'created', ]
        fields = ['text', 'answerfor']
        widgets = {
            'text': forms.Textarea(
            attrs={
                'id': 'create_post_text',
                'required': True,
                'placeholder': "What's new?",
                'name' : 'the_post',
                'cols': 50,
                'rows' : 5,
            }),
        }

    def clean_text(self):
        text = self.cleaned_data['text']
        if not text:
            raise ValidationError(
                ('Enter something, empty posts are not cool!'),
                code='invalid',
            )
        return text


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'website', 'picture')

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if isinstance(first_name, str):
            first_name = first_name.encode('ascii', 'xmlcharrefreplace')
            if not 3 <= len(first_name) <= 30:
                raise ValidationError(
                ('%(value)s must be more than 2 and less than 30 chars length!') % {'value': 'First name'},
                code='invalid',
                )
            return first_name
        else:
            raise ValidationError(
                ('Invalid value: %(value)s') % {'value': 'First name'},
                code='invalid',
            )

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if isinstance(last_name, str):
            last_name = last_name.encode('ascii', 'xmlcharrefreplace')
            if not 3 <= len(last_name) <= 30:
                raise ValidationError(
                ('%(value)s must be more than 2 and less than 30 chars length!') % {'value': 'Last name'},
                code='invalid',
                )
            return last_name
        else:
            raise ValidationError(
                ('Invalid value: %(value)s') % {'value': 'Last name'},
                code='invalid',
            )

    def clean_picture(self):
        avatar = self.cleaned_data['picture']
        if avatar:
            w, h = get_image_dimensions(avatar)
        else:
            return

        #validate dimensions
        max_width = max_height = 500
        if w > max_width or h > max_height:
            raise forms.ValidationError(
                u'Please use an image that is '
                 '%s x %s pixels or smaller.' % (max_width, max_height))

        #validate content type
        main_type, sub = avatar.content_type.split('/')
        if not (main_type == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
            raise forms.ValidationError(u'Please use a JPEG, '
                'GIF or PNG image.')

        #validate file size
        if len(avatar) > (1024 * 1024):
            raise forms.ValidationError(
                u'Avatar file size may not exceed 1kk.')