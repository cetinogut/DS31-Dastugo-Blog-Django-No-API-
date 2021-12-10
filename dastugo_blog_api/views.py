from rest_framework import generics
from rest_framework import permissions
from dastugo_blog_app.models import Post
from .serializers import PostSerializer
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated,IsAdminUser, DjangoModelPermissionsOrAnonReadOnly, DjangoModelPermissions, BasePermission, IsAuthenticatedOrReadOnly
from rest_framework import viewsets
from rest_framework import filters
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

class PostUserWritePermission(BasePermission):
    message = 'Editing posts is restricted to the blogger only.'

    def has_object_permission(self, request, view, obj): # this is an custom permission and only auth users can edit their own posts
        if request.method in SAFE_METHODS: # get, option or had
            return True # read only 
        return obj.blogger == request.user

class PostList(viewsets.ModelViewSet):
    permission_classes = [PostUserWritePermission]
    serializer_class = PostSerializer
    #queryset = Post.objects.all()  # this 4 lines do all listing and detail calls
    #instead of default queryset  above we can define a custom one as below... only one can be used
    
    # Define Custom Queryset
    def get_queryset(self):
        return Post.objects.all()
    
    # by default the above modelviewset can retrive api/3/ i.e id numbers of blog posts .But if we want ot get posts by title we can define a custom get function as below..
    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(Post, slug=item)

    

#####ViewSet ####
""" class PostList(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    #queryset = Post.posted_objects.all() # this filtered one did not work, look for the bug..
    queryset = Post.objects.all()

    def list(self, request):
        serializer_class = PostSerializer(self.queryset, many=True)
        return Response(serializer_class.data)

    def retrieve(self, request, pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        serializer_class = PostSerializer(post)
        return Response(serializer_class.data) """

    # def list(self, request):
    #     pass

    # def create(self, request):
    #     pass

    # def retrieve(self, request, pk=None):
    #     pass

    # def update(self, request, pk=None):
    #     pass

    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     pass
    
######Generic Views####
""" 
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
 """

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