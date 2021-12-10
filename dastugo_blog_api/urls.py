from django.urls import path
#from .views import PostList, PostDetail # was used for generic views
from .views import PostList
from rest_framework.routers import DefaultRouter

app_name = 'dastugo_blog_api'

router = DefaultRouter()
router.register('', PostList, basename='post')
urlpatterns = router.urls #declaring that we'll use router.urls insetad of url patterns below

""" urlpatterns = [
    path('<int:pk>/', PostDetail.as_view(), name='detail-create'),
    path('', PostList.as_view(), name='list-create'),
] """