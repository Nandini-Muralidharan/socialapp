from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models import Count

class Posts(models.Model):
    
    title=models.CharField(max_length=200)
    image=models.ImageField(upload_to="images",null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateField(auto_now_add=True)
    liked_by=models.ManyToManyField(User,related_name="liked_by")

    @property
    def posts_comments(self):
       #return self.comments_set.all()
       qs=self.comments_set.all()
       return qs

   
    
    def __str__(self):
        return self.title

    @property
    def likecount(self):
        return self.liked_by.all().count()
    




class Comments(models.Model):
 
    post=models.ForeignKey(Posts,on_delete=models.CASCADE)
    comments=models.CharField(max_length=200)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateField(auto_now_add=True)


    def __str__(self):
        return self.comments


class Userprofile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    profile_pic=models.ImageField(upload_to="profile_pics",null=True)
    timelinepic=models.ImageField(upload_to="timelinepic",null=True)
    followings=models.ManyToManyField(User,related_name="followings")


class Friends(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    date = models.DateTimeField(auto_now_add=True)