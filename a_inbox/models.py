from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from django.utils.timesince import timesince
# Create your models here.

''' the relationship specified by sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages") indicates a "many-to-one" relationship between the InboxMessage table and the User table.

In a many-to-one relationship:

"Many" refers to the fact that one user can have multiple inbox messages (or sent messages in this case).
"One" refers to the fact that each inbox message is associated with exactly one user (the sender).
So, to clarify:

The "many" side is represented by the InboxMessage model, as it can have many instances associated with a single user.
The "one" side is represented by the User model, as each inbox message is sent by exactly one user.
In simpler terms, each inbox message belongs to one user (the sender), but one user can have many inbox messages. '''

class InboxMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    conversation = models.ForeignKey("Conversation", on_delete=models.CASCADE, related_name="messages")
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        
    def __str__(self):
        time_since = timesince(self.created, timezone.now())
        return f'{self.sender.username} : {time_since} ago '
    
class Conversation(models.Model):
    id = models.CharField(max_length=150, default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    participants = models.ManyToManyField(User, related_name="conversations")
    lastmessage_created = models.DateField(default=timezone.now())
    is_seen = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-lastmessage_created']
        
    def __str__(self):
        user_names = ", ".join( user.username for user in self.participants.all())
        return f"[ {user_names} ]"