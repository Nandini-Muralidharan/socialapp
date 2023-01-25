from django.urls import path
from socialwebb.views import SignInView,SignUpView,IndexView,add_comments,post_liked_by_view,signout_View,AddProfileView,ViewmyprofileView,ProfileView,EditprofileView,post_delete,add_follower,ListPeopleView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("login",SignInView.as_view(),name="signin"),
    path("register",SignUpView.as_view(),name="signup"),
    path("index",IndexView.as_view(),name="index"),
    path("posts/<int:id>/comments/add",add_comments,name="add-comments"),
    path("comments/<int:id>/liked_by/add",post_liked_by_view,name="liked_by-add"),
    path("logout",signout_View,name="sign-out"),
    path("profile",AddProfileView.as_view(),name="profile"),
    path("myprofile",ViewmyprofileView.as_view(),name="myprofile"),
    path("myprofilepost",ProfileView.as_view(),name="myprofilepost"),
    path("users/profile/<int:id>/change",EditprofileView.as_view(),name="edit-profile"),
    path("post/<int:id>/remove",post_delete,name="post-delete"),
    path("user/<int:id>/follower/add",add_follower, name="add-follower"),
    path("people/", ListPeopleView.as_view(),name="people"),

  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
