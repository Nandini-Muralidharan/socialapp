from django.shortcuts import render

# Create your views here.
from socialnetworkapp.serializers import UserSerializer,PostsSerializer,CommentsSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth.models import User
from socialnetworkapp.models import Posts,Comments
from rest_framework import authentication,permissions
from rest_framework.decorators import action

class UserView(ModelViewSet):

    serializer_class=UserSerializer
    queryset=User.objects.all()


class PostsView(ModelViewSet):
    serializer_class=PostsSerializer
    queryset=Posts.objects.all()
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    #localhost:8000/posts/1/liked_by/

    @action(methods=["get"],detail=True)
    def likes(self,request,*arg,**kw):
        pos=self.get_object()
        usr=request.user
        pos.liked_by.add(usr)
        return Response(data="liked")





    


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    #list all posts
    #localhost:8000/posts/

    @action(methods=["GET"],detail=False)
    def my_posts(self,request,*arg,**kw):
        qs=request.user.posts_set.all()
        serializer=PostsSerializer(qs,many=True)
        return Response(data=serializer.data)

    #addcomments
    #localhost:8000/posts/1/add_comments/

    @action(methods=["POST"],detail=True)
    def add_comments(self,request,*arg,**kw):
        id=kw.get("pk")
        pos=Posts.objects.get(id=id)
        usr=request.user
        serializer=CommentsSerializer(data=request.data,context={"post":pos,"user":usr})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    #list specific comments
    #localhost:8000/1/list_comments/
    

    @action(methods=["GET"],detail=True)
    def list_comments(self,request,*arg,**kw):
        id=kw.get("pk")
        pos=Posts.objects.get(id=id)
        qs=pos.comments_set.all()
        serializer=CommentsSerializer(qs,many=True)
        return Response(data=serializer.data)



    #list post_comments
    #localhost:8000/posts[models]

class CommentView(ModelViewSet):
    serializer_class=CommentsSerializer
    queryset=Comments.objects.all()
    authentication_classes=[authentication.BasicAuthentication]  
    permission_classes=[permissions.IsAuthenticated]



     



    
