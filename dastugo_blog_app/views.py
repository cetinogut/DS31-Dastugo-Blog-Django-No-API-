from django.shortcuts import get_object_or_404, redirect, render
from .models import Post, Like, PostView
from .forms import CommentForm, PostForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import generic # imports all generic including  ListView , DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

def post_list(request):
    posts = Post.objects.filter(status='p') # bring the published posts
    context = {
        "post_list": posts
    }
    print(posts)
    print(context)
    return render(request, "dastugo_blog_app/post_list.html", context)

def home(request):
    current_url = request.resolver_match.url_name
    
    print(current_url)
    context = {
        "current_url" : current_url
    }
    return render(request, "dastugo_blog_app/index.html", context)

def about(request):
    current_url = request.resolver_match.url_name
    
    print(current_url)
    context = {
        "current_url" : current_url
    }
    return render(request, "dastugo_blog_app/about.html", context)

def contact(request):
    current_url = request.resolver_match.url_name
    print(current_url)
    context = {
        "current_url" : current_url
    }
    return render(request, "dastugo_blog_app/contact.html", context)

""" class HomeView(generic.ListView): #this home page works as post list view
   model = Post
   template_name = 'dastugo_blog_app/post_list.html'
   paginate_by = 4 """
   
def post_detail(request, slug):
    form = CommentForm()
    post_object = get_object_or_404(Post, slug=slug)
    
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
            return redirect("dastugo_blog_app:post-detail", slug=slug) # affter commenting remain at the same page
            # return redirect(request.path)
    context = {
        "post": post_object,
        "like": like_qs, # to check if the user already liked the post
        "form": form
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