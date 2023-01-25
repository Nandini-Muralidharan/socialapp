from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from socialnetworkapp.models import Posts,Userprofile



class PostForm(forms.ModelForm):
   
    class Meta:
        model=Posts
        fields=["title","image"]
        
        widgets={
            "title":forms.TextInput(attrs={"class":"form-control border bs-0 "}),
            "image":forms.FileInput(attrs={"class":"form-select"})
        }


class ProfileForm(forms.ModelForm):
    
    class Meta:
        model= Userprofile
        fields=["profile_pic","timelinepic"]

       

class UserRegistrationForm(UserCreationForm):
   
    class Meta:
        model=User
        fields=["first_name","last_name","username","email","password1","password2"]


class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()


