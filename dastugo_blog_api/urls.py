from django.urls import path
from .views import PostDetailWithSlugFromParams, PostListDetailFilter,PostDetailWithSlug, PostSearchBlogger, PostList, PostListAllPublished, PostListForBlogger, PostDetailWithId, PostDetailWithId2, CreatePost, EditPost, AdminPostDetail, DeletePost #, PostDetailWithSlug,  # was used for generic views
#from .views import PostList # if use router, we only need this view, if use urlpatterns use the views above
from rest_framework.routers import DefaultRouter

app_name = 'dastugo_blog_api'

router = DefaultRouter()
router.register('', PostList, basename='post') # all three http://127.0.0.1:8000/api/, http://127.0.0.1:8000/api/16, http://127.0.0.1:8000/api/lastweek-serap-software-kasm-32686ccd31/
#router.register(r'posts', PostList) URL pattern: ^posts/$ Name: 'post-list', URL pattern: ^posts/{pk}/$ Name: 'post-detail'
#urlpatterns = router.urls #declaring that we'll use router.urls insetad of url patterns below

urlpatterns = [
    path('<int:pk>/', PostDetailWithId.as_view(), name='detail-create-post-id'), #http://127.0.0.1:8000/api/1/
    path('single/<int:pk>/', PostDetailWithId2.as_view(), name='detail-create-post-id2'), #http://127.0.0.1:8000/api/10/
    path('single/<str:slug>/', PostDetailWithSlug.as_view(), name='detail-create-post-slug'), #http://127.0.0.1:8000/api/single/serap-new-blog-sunday-morning-d8d2e626e9/
    path('posts/', PostDetailWithSlugFromParams.as_view(), name='detail-create'), # http://127.0.0.1:8000/api/posts/?slug=dogan-blog-2-selamlar-dogut, this view get the param from request url, thats why we don't have any parameters after "posts/"
    path('postspublished', PostListAllPublished.as_view(), name='list-create'), # http://127.0.0.1:8000/api/postspublished
    path('bloggerposts/', PostListForBlogger.as_view(), name='list-create-for-blogger'), # http://127.0.0.1:8000/api/bloggerposts/
    path('search/', PostListDetailFilter.as_view(), name='post-search'),# http://127.0.0.1:8000/api/search/?search=dogan
    #path('search2/', PostSearchBlogger.as_view(), name='post-search-blogger'), test this part
    # Post Admin URLs
    path('admin/create/', CreatePost.as_view(), name='create-post'),
    path('admin/edit/postdetail/<int:pk>/', AdminPostDetail.as_view(), name='admin--'),
    path('admin/edit/<int:pk>/', EditPost.as_view(), name='edit-post'),
    path('admin/delete/<int:pk>/', DeletePost.as_view(), name='delete-post'),
]

urlpatterns += router.urls # include router urls as well