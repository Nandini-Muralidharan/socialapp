from django.shortcuts import render,redirect

# Create your views here.
from django.views.generic import CreateView,FormView,TemplateView,ListView,UpdateView
from socialwebb.forms import LoginForm,UserRegistrationForm,PostForm,ProfileForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from socialnetworkapp.models import Posts,Comments,Userprofile,Friends
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User



def signin_required(fn):
    def wrapper(request,*arg,**kw):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")
        else:
            return fn(request,*arg,**kw)
    return wrapper



decs=[signin_required,never_cache]

class SignUpView(CreateView):
    template_name="register.html"
    form_class=UserRegistrationForm
    success_url=reverse_lazy("signin")


class  SignInView(FormView):
    template_name="login.html"
    form_class=LoginForm


    def post(self,request,*arg,**kw):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pswd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pswd)
            if usr:
                login(request,usr)
                return redirect("index")
            else:
                 print("signup")
                 return render(request,self.template_name,{"form":form})

          
@method_decorator(decs,name="dispatch")
class IndexView(CreateView,ListView):
    template_name="index.html"
    form_class=PostForm
    success_url=reverse_lazy("index")
    model=Posts
    queryset = Posts.objects.all().order_by('-created_date')
    context_object_name="posts"



    def form_valid(self,form):
        form .instance.user=self.request.user
        messages.success(self.request,"your posts added successfully")
        return super().form_valid(form)

    # def get_queryset(self):
    #     return Posts.objects.exclude(user=self.request.user).order_by("-created_date")




def add_comments(request,*arg,**kw):
    id=kw.get("id")
    pos=Posts.objects.get(id=id)
    c=request.POST.get("comments")
    Comments.objects.create(post=pos,comments=c,user=request.user)
    return redirect("index")


def post_liked_by_view(request,*arg,**kw):
    id=kw.get("id")
    pos=Posts.objects.get(id=id)
    pos.liked_by.add(request.user)
    return redirect("index")

class AddProfileView(CreateView):
    template_name="profile.html"
    form_class=ProfileForm
    success_url=reverse_lazy("index")
    context_object_name="posts"
    queryset=Posts.objects.all()

    def post(self, request,*args,**kw):
        form=ProfileForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            profile=form.save(commit=False)
            profile.user=request.user
            profile.save()
            return redirect("index")
        else:
            return render(request,"profile.html",{"form":form})

decs   
class ProfileView(ListView):
    template_name="myprofilepost.html"
    form_class=PostForm
    model=Posts
    success_url=reverse_lazy("index")
    context_object_name="posts"
    queryset=Posts.objects.all()

    def get_queryset(self):
        return Posts.objects.filter(user=self.request.user).order_by("-created_date")
    

    

class ViewmyprofileView(TemplateView):
    template_name="profileview.html"


    # class PostListView(ListView):
    # template_name="myprofile.html"
    
    # model=Posts
    
    # context_object_name="posts"
    # queryset=Posts.objects.all()

    # def get_queryset(self):
    #     return Posts.objects.filter(user=self.request.user).order_by("-created_date")
# 

decs
class EditprofileView(UpdateView):
    template_name="edit.html"
    form_class=ProfileForm
    model=Userprofile
    pk_url_kwarg="id"
    success_url=reverse_lazy("listpost")





def signout_View(request,*arg,**kw):
    logout(request)
    return redirect("signin")



def post_delete(request,*args,**kw):
    id=kw.get("id")
    Posts.objects.get(id=id).delete()

    return redirect("index")


class ListPeopleView(ListView):
    template_name="peoples.html"
    model=User
    context_object_name = 'people'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["followings"] = Friends.objects.filter(follower=self.request.user)
        context["posts"] = Posts.objects.all().order_by('-created_date')
        return context
    

    def get_queryset(self):
        return User.objects.exclude(username=self.request.user)


def add_follower(request, *args, **kwargs):
    id = kwargs.get('id')
    usr = User.objects.get(id=id)
    if not Friends.objects.filter(user=usr, follower=request.user):
        Friends.objects.create(user=usr, follower=request.user)
    else:
        Friends.objects.get(user=usr, follower=request.user).delete()
    return redirect("people")


def post_delete(request,*args,**kw):
    id=kw.get("id")
    Posts.objects.get(id=id).delete()
    return redirect("index")




