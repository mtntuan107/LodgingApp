import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField


class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m')
    dob = models.DateField(auto_now=False, auto_now_add=False, default=None)
    phone_number = models.CharField(max_length=10, null=False, default="113")
    role = models.CharField(max_length=10, null=False, default="user")


class Owner(User):
    cmt = models.CharField(max_length=10, null=False, default="chu")


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class ImageOwner(BaseModel):
    image = models.ImageField(upload_to='uploads/%Y/%m')
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)


class Lodging(BaseModel):
    title = models.CharField(max_length=255, default="New Lodging")
    locate = models.CharField(max_length=100, null=False)
    e_price = models.IntegerField(default=1)
    w_price = models.IntegerField(default=1)
    description = RichTextField(default=None)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class ImageLodging(BaseModel):
    image = models.ImageField(upload_to='uploads/%Y/%m')
    lodging = models.ForeignKey(Lodging, on_delete=models.CASCADE)


class SPrice(BaseModel):
    name = models.CharField(max_length=100, null=False, unique=True)
    value = models.IntegerField()

    lodging = models.ForeignKey(Lodging, on_delete=models.CASCADE)


class Post(BaseModel):
    title = models.CharField(max_length=255, default="New post")
    area = models.CharField(max_length=100, null=False) #
    price = models.IntegerField(default=1)
    content = RichTextField(default=None)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Follow(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='follower')
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'owner')
        ordering = ['-followed_at']

    def __str__(self):
        return f"{self.user.username} follows {self.owner.user.username}"


class Comment(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.owner.user.username} on {self.post.title}'

    class Meta:
        ordering = ['-created_at']


class CommentUL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_lodging')
    lodging = models.ForeignKey(Lodging, on_delete=models.CASCADE, related_name='comments_lodging')
    content = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.lodging.title}'

    class Meta:
        ordering = ['-created_at']