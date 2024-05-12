from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from a_users.models import Profile
from django.http import HttpResponse, Http404
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def inbox_view(request, conversation_id=None):
    my_conversation = Conversation.objects.filter(participants = request.user)
    if conversation_id:
        conversation = get_object_or_404(my_conversation, id = conversation_id)
        latest_message = conversation.messages.first()
        if conversation.is_seen == False and latest_message.sender != request.user:
            conversation.is_seen = True
            conversation.save()
    else:
        conversation = None   
    context = {
        'conversation' : conversation,
        'my_conversation' : my_conversation
    }
    return render(request, 'a_inbox/inbox.html', context)

@login_required
def search_users_view(request):
    letters = request.GET.get('search_user')
    if request.htmx:
        if len(letters) > 0:
            
            profiles = Profile.objects.filter(realname__icontains=letters).exclude(realname = request.user.profile.realname)

            users_id = profiles.values_list('user', flat=True)
            
            users = User.objects.filter(
                Q(username__startswith=letters) | Q(id__in = users_id)
            ).exclude(username = request.user.username)
            
            return render(request, 'a_inbox/list_searchusers.html', {'users' : users})
        else:
            return HttpResponse('')
    else:
        raise Http404()

@login_required
def new_message(request, recipient_id):
    recipient = get_object_or_404(User, id = recipient_id)
    new_message_form = InboxNewMessageForm()
    
    if request.method == 'POST':
        
        form = InboxNewMessageForm(request.POST)
        if form.is_valid():
            
            message = form.save(commit=False)
            message.sender = request.user

            my_conversations = request.user.conversations.all()
            
            for c in my_conversations:
                
                if recipient in c.participants.all():
                    
                    message.conversation = c
                    message.save()
                    
                    c.lastmessage_created = timezone.now()
                    c.is_seen = False
                    c.save()
                    
                    return redirect('inbox', c.id)

            new_conversation = Conversation.objects.create()
            new_conversation.lastmessage_created = timezone.now()
            new_conversation.participants.add(request.user, recipient)
            new_conversation.save()
            
            message.conversation = new_conversation
            message.save()
            
            return redirect('inbox', new_conversation.id)              
    
    context = {'new_message_form' : new_message_form, 'recipient' : recipient}
    
    return render(request, 'a_inbox/form_newmessage.html', context)
     
@login_required    
def new_reply(request, conversation_id):
    
    new_reply_form = InboxNewMessageForm()
    my_conversation = request.user.conversations.all()

    conversation = get_object_or_404(my_conversation, id = conversation_id )
    
    if request.method == 'POST':
        form = InboxNewMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.conversation = conversation
            message.save()
            
            conversation.lastmessage_created = timezone.now()
            conversation.is_seen = False
            conversation.save()
            
            return redirect('inbox', conversation.id)

    context = { 'new_reply_form' : new_reply_form, 'conversation' : conversation}
    return render(request, 'a_inbox/form_newreply.html', context)
    
    
@login_required
def notify_newmessage(request, conversation_id):
    conversation = get_object_or_404(Conversation, id = conversation_id)
    latest_message = conversation.messages.first()
    if conversation.is_seen == False and latest_message.sender != request.user:
        return render(request, 'a_inbox/notify_icon.html')
    else:
        return HttpResponse('')
    
def notify_inbox(request):
    my_conversation = Conversation.objects.filter(participants=request.user, is_seen=False)
    for c in my_conversation:
        latest_message = c.messages.first()
        if latest_message.sender != request.user:
            return render(request, 'a_inbox/notify_icon.html')
    else:
        return HttpResponse('') 
    