from django.db import models
import uuid
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    author = models.ForeignKey( User, on_delete=models.SET_NULL, null=True, related_name='posts' )
    title = models.CharField( max_length=500)
    artist = models.CharField( max_length=500 , null=True)
    url = models.URLField(max_length=500, null=True)
    image = models.URLField( max_length=500)
    tags = models.ManyToManyField("Tag")
    body = models.TextField()
    likes = models.ManyToManyField(User, related_name="likedposts", through="LikedPost")
    created = models.DateTimeField(auto_now=True, auto_now_add=False)
    id = models.CharField( max_length=100 , default= uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-created']
        
    # def get_absolute_url(self):
    #     return reverse("Post_detail", kwargs={"pk": self.pk})

class LikedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'{self.user.username} : {self.post.title}'

class Tag(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True)
    image = models.FileField(upload_to='icons/', null=True, blank=True)
    class Meta:
        pass
    def __str__(self):
        return self.name
    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="comments")
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    body = models.CharField(max_length=150)
    likes = models.ManyToManyField(User, related_name="likedcomments", through="LikedComment")
    created = models.DateTimeField(auto_now=True)
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    
    def __str__(self):
        try:
            return f'{self.author.username} : {self.body[:30]}' 
        except:
            return f'no author : {self.body[:30]}' 
     
    class Meta:
        ordering = ['-created']       


class LikedComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'{self.user.username} : {self.comment.body[:30]}'

class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="replies")
    parent_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="replies")
    body = models.CharField(max_length=150)
    likes = models.ManyToManyField(User, related_name="likedreplies", through="LikedReply")
    created = models.DateTimeField(auto_now=True)
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    
    def __str__(self):
        try:
            return f'{self.author.username} : {self.body[:30]}' 
        except:
            return f'no author : {self.body[:30]}' 
     
    # class Meta:
    #     ordering = ['-created']       
    
class LikedReply(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'{self.user.username} : {self.reply.body[:30]}'

