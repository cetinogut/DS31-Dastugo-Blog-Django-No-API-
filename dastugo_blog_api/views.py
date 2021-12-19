from rest_framework import generics
from rest_framework import permissions
from dastugo_blog_app.models import Post
from .serializers import PostSerializer
from rest_framework.permissions import SAFE_METHODS, AllowAny,IsAuthenticated,IsAdminUser, DjangoModelPermissionsOrAnonReadOnly, DjangoModelPermissions, BasePermission, IsAuthenticatedOrReadOnly
from rest_framework import viewsets
from rest_framework import filters #added for search functionality
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView ## added during the new imp. for image upload
from rest_framework import status  ## added during the new imp. for image upload
from rest_framework.parsers import MultiPartParser, FormParser ## added during the new imp. for image upload

class PostUserWritePermission(BasePermission):
    message = 'Editing posts is restricted to the blogger only.'

    def has_object_permission(self, request, view, obj): # this is an custom permission and only auth users can edit their own posts
        if request.method in SAFE_METHODS: # get, option or had
            return True # read only 
        return obj.blogger == request.user

### model viewset works with router better, since commented route in urls.py, commented here as well. other wise it will generate The `actions` argument must be provided when calling `.as_view()` on a ViewSet. For example `.as_view({'get': 'list'})` error.  Refer to django-rest-framework docs
class PostList(viewsets.ModelViewSet): # http://127.0.0.1:8000/api/ and http://127.0.0.1:8000/api/16/ and http://127.0.0.1:8000/api/lastweek-serap-software-kasm-32686ccd31/ because of routers # returns all posts with get_queryset, and post slugs withget_object
    permission_classes = [PostUserWritePermission] # user can see all posts in list  and detail but edits only own posts
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

class PostListForBlogger(generics.ListAPIView): # a custom view for filtering blog posts of a logged-in user
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(blogger=user)

class PostDetailWithSlugFromParams(generics.ListAPIView): # get the slug from frontend params and return related post from backend, this is a search filter like view and only worls with ListViews not with RetrieveViews
    serializer_class = PostSerializer

    def get_queryset(self):
        slug = self.request.query_params.get('slug', None)
        print(slug)
        return Post.objects.filter(slug=slug) # http://127.0.0.1:8000/api/posts/?slug=dogan-blog-2-selamlar-dogut

class PostListDetailFilter(generics.ListAPIView): # this is for search facility coming fro mReact Search Bar.

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^slug']

    # '^' Starts-with search.
    # '=' Exact matches.
    # '@' Full-text search. (Currently only supported Django's PostgreSQL backend.)
    # '$' Regex search.

class PostSearchBlogger(generics.ListAPIView): # created for blogger search, not in use
    permission_classes = [AllowAny]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^blogger'] 

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

class PostListAllPublished(generics.ListCreateAPIView, ):
    #permission_classes= [IsAdminUser] # view level permission based on model
    #permission_classes= [DjangoModelPermissionsOrAnonReadOnly]
    #permission_classes= [DjangoModelPermissions]
    permission_classes= [IsAuthenticatedOrReadOnly]
    #queryset = Post.posted_objects.all() ##smth wrong the list coming empty
    queryset = Post.objects.filter(status="p")
    serializer_class = PostSerializer

class PostDetailWithId(generics.RetrieveUpdateDestroyAPIView, PostUserWritePermission): # default view filtering with pk
    permission_classes= [PostUserWritePermission]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetailWithId2(generics.ListAPIView): # a custom view for filtering blog posts of a logged-in user
    #permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        post_id = self.kwargs['pk']
        print(post_id)
        return Post.objects.filter(id=post_id)
    
class PostDetailWithSlug(generics.ListAPIView): # a custom view for filtering blog posts of a logged-in user
    #permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        post_slug = self.kwargs['slug']
        print(post_slug)
        return Post.objects.filter(slug=post_slug)

# Post Admin all requires being logged in.

""" class CreatePost(generics.CreateAPIView): #in order to upload image we chnaged the implementation as below
    #permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer # we are using our generic serializer """

class CreatePost(APIView): # added for a new implementation of image upload
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser] # image + form text data we need multipartparser 

    def post(self, request, format=None):
        print(request.data) # we can get bad request 400, this is because we are not sending correct data format to serialize and this can be checked here by printing on the console 
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AdminPostDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class EditPost(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

class DeletePost(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    
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