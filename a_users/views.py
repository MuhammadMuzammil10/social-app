from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import *
from a_inbox.forms import InboxNewMessageForm
from django.contrib import messages
from a_posts.models import *
from a_posts.forms import ReplyCreateForm
from django.db.models import Count
# Create your views here.

def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username = username).profile
    else:
        try:
            profile = request.user.profile
        except:
            raise Http404()
   
    posts = profile.user.posts.all()
    new_message_form = InboxNewMessageForm()
    
    if request.htmx:
        
        if 'top-posts' in request.GET:
            posts = profile.user.posts.annotate(num_likes = Count('likes')).filter(num_likes__gt = 0).order_by('-num_likes')
        
        elif 'top-comments' in request.GET:
            comments = profile.user.comments.annotate(num_likes = Count('likes')).filter(num_likes__gt = 0).order_by('-num_likes')
            replyform = ReplyCreateForm()
            return render(request, 'snippets/loop_profile_comments.html', {'comments':comments, 'replyform' : replyform})
        
        elif 'liked-posts' in request.GET:
            posts = profile.user.likedposts.order_by('-likedpost__created')
            
        return render(request, 'snippets/loop_profile_posts.html', {'posts':posts})
            
    context = {'profile' : profile, 'posts' : posts, 'new_message_form' : new_message_form, 'post' : 'post'}
    context['path'] = request.path.strip('/').split('/')
    context['author'] = username
    return render(request, 'a_users/profile.html',context )

@login_required
def profile_edit_view(request):
    form = ProfileForm(instance=request.user.profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    
    if request.path == reverse('profile-onboarding'):
        template = 'a_users/profile_onboarding.html'
    else:
        template = 'a_users/profile_edit.html'
    return render(request, template , {'form' : form})

@login_required
def profile_delete_view(request):
    user = request.user
    if request.method == "POST":
        logout(request)    
        user.delete()
        messages.success(request, 'Account deleted, what a pity')
        return redirect('home')

    return render(request, 'a_users/profile_delete.html')