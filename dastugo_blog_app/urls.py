from django.urls import path
from .views import home,index_post_list, about, contact, post_detail, post_list, post_create, post_update, post_delete, like  
#from .views import HomeView, PostCreate


app_name = "dastugo_blog_app" # if we have more than one apps to have a better routing we wil luse the app name before the route.
urlpatterns = [
    #path('', HomeView.as_view(), name='post-list'),
    path("", post_list, name="post-list"),
    #path("index/", home, name="home"),
    path("index/", index_post_list, name="home"),
    path("about/", about, name="about"),
    path("contact/", contact, name="contact"),
    path("create/", post_create, name="post-create"),
    #path("create/", PostCreate.as_view(), name="post-create"),
    path("<str:slug>/", post_detail, name="post-detail"),
    path("update/<str:slug>/", post_update, name="post-update"),
    path("delete/<str:slug>/", post_delete, name="post-delete"),
    path("like/<str:slug>/", like, name="like"),
    
    
]