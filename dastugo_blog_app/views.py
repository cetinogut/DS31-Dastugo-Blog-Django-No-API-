from django.shortcuts import get_object_or_404, redirect, render
from .models import Post, Like, PostView, Category
from django.views import generic # imports all generic including  ListView , DetailView
from .forms import CommentForm, PostForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import generic # imports all generic including  ListView , DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Count
from datetime import datetime, date, timedelta

# functional views for training
def home(request):
    current_url = request.resolver_match.url_name
    
    print(current_url)
    context = {
        "current_url" : current_url # this was a test to carry out passing info to home page via context
    }
    return render(request, "dastugo_blog_app/index.html", context)

def post_list(request): # this is for a table list in a staff view.. in the old version it was listing the posts in the index page
    posts = Post.objects.filter(status='p') # bring the published posts
    context = {
        "post_list": posts
    }
    #print(posts)
    #print(context)
    return render(request, "dastugo_blog_app/post_list.html", context)

def index_post_list(request): # this is for the complex index page of the weblog
    posts = Post.objects.filter(status='p') # bring the published posts
    recent_post_list = Post.objects.all().order_by('-publish_date')[:6] # first six posts in the slider
    last_post = Post.objects.first() #since reverse ordered based on publish date, first birings the latest post
    category_list = Category.objects.all()
    
    # a list of latest post in each category
    latest_posts_on_each_category = []
    for category in category_list: # refactor this to another function and render directly fro mthis function 
         latest_on_that_category = posts.filter(category = category).first()
         latest_posts_on_each_category.append(latest_on_that_category)
    
    #most liked post
    most_liked_post_dict = Like.objects.all().values('post').annotate(total=Count('post')).order_by('-total').first()
    #print(list(most_liked_post_dict.keys())[0])
    #print(list(most_liked_post_dict.values())[0])
    most_liked_post = Post.objects.get(pk=list(most_liked_post_dict.values())[0])
    #print(most_liked_post)
    
    #most read post
    most_read_post_dict = PostView.objects.all().values('post').annotate(total=Count('post')).order_by('-total').first()
    #print(list(most_read_post_dict.keys())[0])
    #print(list(most_read_post_dict.values())[0])
    most_read_post = Post.objects.get(pk=list(most_read_post_dict.values())[0])
    #print(most_read_post)
    
    #popular posts
    #popular_posts = Post.objects.order_by('-postview')[:5]
    popular_posts = Post.objects.annotate(readlike_count=Count('postview') + Count('like')).filter(readlike_count__gt=2)[:5]
    #print(popular_posts)
    #print(recent_post_list)
    print(last_post.title)
    print(last_post.slug)
    print('test')
    
    #sample query
    # documents = Document.objects.all().filter(course_name__courses__iexact=file_name)
    # context["documents"] = documents
    #this part is for the slideri nside the left part of the index.html
    
        
    context = {
        "post_list": posts,
        "recent_post_list": recent_post_list,
        "last_post": last_post,
        "category_list": category_list,
        "latest_posts_on_each_category" : latest_posts_on_each_category,
        'most_liked_post': most_liked_post,
        'most_read_post': most_read_post,
        'popular_posts':popular_posts
        
    }
    #print(posts)
    #print(context)
    return render(request, "dastugo_blog_app/index_post_list.html", context)

def about(request):
    current_url = request.resolver_match.url_name
    
    print(current_url)
    context = {
        "current_url" : current_url
    }
    return render(request, "dastugo_blog_app/about.html", context)

def contact(request):
    """ current_url = request.resolver_match.url_name
    print(current_url)
    context = {
        "current_url" : current_url
    } """
    return render(request, "dastugo_blog_app/contact.html")

#@login_required()
def post_detail(request, slug):
    form = CommentForm()
    post_object = get_object_or_404(Post, slug=slug)
    
    #data tobe sent via context to detail page ## need refactoring for the left side. it an be moved to to base_dastugo.html
    posts = Post.objects.filter(status='p').order_by('-publish_date') # bring the published posts
    recent_post_list = posts.order_by('-publish_date')[1:6] # latest 5 posts excluding the last one. Because it is already  posted above
    last_post = posts.first() #since reverse ordered based on publish date, first birings the latest post
    post_numbers_in_each_category = Category.objects.annotate(nblog=Count('post'))
    
    # popular posts of the last week
    popular_posts = posts.annotate(readlike_count=Count('postview') + Count('like')).filter(readlike_count__gt=2)[:5]
    lastweek = date.today() - timedelta(weeks=1) # https://stackoverflow.com/questions/62035327/filtering-posts-from-yesterday-last-week-and-last-month-doesnt-work
    popular_posts_last_week = posts.filter(publish_date__gt=lastweek).annotate(readlike_count=Count('postview') + Count('like')).filter(readlike_count__gte=2)
    print(popular_posts)
    print(popular_posts_last_week)
    
    print("popular posts last week")
       
    if request.user.is_authenticated:
        PostView.objects.create(reader=request.user, post=post_object)
        like_qs = Like.objects.filter(user=request.user, post=post_object) # added here to access whether the user likd this post before. based on the result we show red heart in the template, if the user already liked it.
    else:
        like_qs =[]
        
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid:
            comment = form.save(commit=False)
            comment.commentor = request.user
            comment.post = post_object
            comment.save()
            return redirect("dastugo_blog_app:post-detail", slug=slug) # after commenting remain at the same page
            # return redirect(request.path)
    context = {
        "post": post_object,
        "like": like_qs, # to check if the user already liked the post
        "form": form,
        'recent_post_list': recent_post_list,
        'last_post': last_post,
        'post_numbers_in_each_category' : post_numbers_in_each_category ,
        'popular_posts_last_week':popular_posts_last_week
        
    }
    
    return render(request, "dastugo_blog_app/post_detail.html", context)

@login_required()
def post_create(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        
    #form = PostForm(request.Post or None, request.FILES or None) # does the same thisn as above lines
        if form.is_valid():
            post = form.save(commit=False) # save data from the form but not to db
            post.blogger = request.user # this wii not be shown in the form. We will create it based on current user.
            post.save() # after saving the post, we have an id for this new post now and we can now add new category(ies ) to the related many to many relation ship table below.
            
            selected_cats = form.cleaned_data['category'] # mant to many relations ship requires additional work here
            #print (selected_cats)
            for cat in selected_cats:
                post.category.add(cat)
                
            messages.success(request, "Post created succesfully!")
            return redirect("dastugo_blog_app:post-list") #if it is a POSt method redirect to post-list after saving the new post
    context = {
        'form': form
    }
    return render(request, "dastugo_blog_app/post_create.html", context) # else this is a GET method and stay in the mpth create form

""" class PostCreate(CreateView):
    model = Post
    fields = ['title', 'content', 'blogger', 'category', 'status', 'published_date', 'image']
    initial = {'published_date': '11/06/2020'} """

@login_required()
def post_update(request, slug):
    post_object = get_object_or_404(Post, slug=slug) # slug = "dogan-new-blog-good-sunday-ab1bd59c7c" instead of id use this slug to find our post
    form = PostForm(request.POST or None, request.FILES or None, instance=post_object) # instance is the one we are looking for. and we dont want to lose it.
    # if request.user != post_object.author:
    #     messages.warning(request, "You're not a writer of this post")
    #     return redirect('dastugo_blog_app:post-list')
    if form.is_valid():
        form.save()
        messages.success(request, "Post updated!!")
        return redirect("dastugo_blog_app:post-list")

    context = {
        "post": post_object,
        "form": form
    }
    return render(request, "dastugo_blog_app/post_update.html", context)

@login_required()
def post_delete(request, slug):
    post_object = get_object_or_404(Post, slug=slug)

    if request.user.id != post_object.blogger.id:
        messages.warning(request, "You're not a writer of this post")
        return redirect('dastugo_blog_app:post-list')
    if request.method == "POST":
        post_object.delete()
        messages.success(request, "Post deleted!!")
        return redirect("dastugo_blog_app:post-list")
    context = {
        "post": post_object
    }
    return render(request, "dastugo_blog_app/post_delete.html", context)

@login_required()
def like(request, slug):
    if request.method == "POST":
        obj = get_object_or_404(Post, slug=slug)
        like_qs = Like.objects.filter(user=request.user, post=obj)
        
        if like_qs:
            like_qs[0].delete()
        else:
            Like.objects.create(user=request.user, post=obj)
        return redirect('dastugo_blog_app:post-detail', slug=slug)
    
    return redirect('dastugo_blog_app:post-detail', slug=slug) # if it is a get then redirect to post-detail

# class-based views
""" class HomeView(generic.ListView): #this home page works as post list view
   model = Post
   template_name = 'dastugo_blog_app/post_list.html'
   paginate_by = 4 """

class PostDetailView(generic.DetailView): #not used currently, just a sample ckass-based view
#class PostDetailView(HitCountDetailView): # $ pip install django-hitcount # https://www.yellowduck.be/posts/counting-hits-objects-django/
    model = Post
    # set to True to count the hit
    #count_hit = True
    
    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context.update({
        'category_list_sidebar' : Category.objects.all(),
        #'popular_posts': Post.objects.order_by('-hit_count_generic__hits')[:3],
        'popular_posts': Post.objects.order_by('-get_view_count')[:5],
        })
        return context