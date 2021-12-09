from django.urls import path
from .views import home,index_post_list, about, contact,underconst, post_detail, post_list, post_create, post_update, post_delete, like  
#from .views import HomeView, PostCreate
from . import views
from django.views.generic import TemplateView


app_name = "dastugo_blog_app" # if we have more than one apps to have a better routing we will use the app name before the route.
urlpatterns = [
    #path('', HomeView.as_view(), name='post-list'),
    path("", post_list, name="post-list"), # initial theme 3-column card style listing of blog posts
    path('', TemplateView.as_view(template_name="dastugo_blog_app/index-api.html")),
    #path("index/", home, name="home"),
    path("index/", index_post_list, name="home"), # new theme main page
    path("about/", about, name="about"),
    path("contact/", contact, name="contact"),
    path("underconst/", underconst, name="underconst"),
    path("create/", post_create, name="post-create"),
    #path("create/", PostCreate.as_view(), name="post-create"),
    path('myposts/', views.PostsByBloggerListView.as_view(), name='my-posts'),
    path("<str:slug>/", post_detail, name="post-detail"),
    path("update/<str:slug>/", post_update, name="post-update"),
    path("delete/<str:slug>/", post_delete, name="post-delete"),
    path("like/<str:slug>/", like, name="like"),
]


""" urlpatterns += [
    path('myposts/', views.PostsByBloggerListView.as_view(), name='my-posts'),
    #path(r'borrowed/', views.AllLoanedBooksForLibrarianListView.as_view(), name='all-borrowed-books'),  # Added for challenge
] """
