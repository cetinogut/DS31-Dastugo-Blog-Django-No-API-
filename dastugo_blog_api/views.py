from rest_framework import generics
from rest_framework import permissions
from dastugo_blog_app.models import Post
from .serializers import PostSerializer
from rest_framework.permissions import SAFE_METHODS, IsAdminUser, DjangoModelPermissionsOrAnonReadOnly, DjangoModelPermissions, BasePermission, IsAuthenticatedOrReadOnly

class PostUserWritePermission(BasePermission):
    message = 'Editing posts is restricted to the blogger only.'

    def has_object_permission(self, request, view, obj): # this is an custom permission and only auth users can edit their own posts
        if request.method in SAFE_METHODS: # get, option or had
            return True # read only 
        return obj.blogger == request.user

class PostList(generics.ListCreateAPIView, ):
    #permission_classes= [IsAdminUser] # view level permission based on model
    #permission_classes= [DjangoModelPermissionsOrAnonReadOnly]
    #permission_classes= [DjangoModelPermissions]
    permission_classes= [IsAuthenticatedOrReadOnly]
    #queryset = Post.posted_objects.all() ##smth wrong the list coming empty
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView, PostUserWritePermission):
    permission_classes= [PostUserWritePermission]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


""" Concrete View Classes
#CreateAPIView
Used for create-only endpoints.
#ListAPIView
Used for read-only endpoints to represent a collection of model instances.
#RetrieveAPIView
Used for read-only endpoints to represent a single model instance.
#DestroyAPIView
Used for delete-only endpoints for a single model instance.
#UpdateAPIView
Used for update-only endpoints for a single model instance.
##ListCreateAPIView
Used for read-write endpoints to represent a collection of model instances.
RetrieveUpdateAPIView
Used for read or update endpoints to represent a single model instance.
#RetrieveDestroyAPIView
Used for read or delete endpoints to represent a single model instance.
#RetrieveUpdateDestroyAPIView
Used for read-write-delete endpoints to represent a single model instance.
"""