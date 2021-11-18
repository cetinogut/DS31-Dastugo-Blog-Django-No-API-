from django.db import models
from datetime import date, datetime
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User #Blog author or commenter
from .utils import get_random_digit # to generate a randon one digit number for comment, like view count at the initial stage


def user_directory_path(instance, filename): # creates a folder named after blogger id in media folder for user uploaded images
    return 'blog_pics/{0}/{1}'.format(instance.blogger.id, filename)


class Category(models.Model):
    """
    Model representing a post category. Each post can have more than one category
    """
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Post(models.Model):
    """
    Model representing a blog post.
    """
    STATUS = (
        ('d',"Draft"),
        ('p',"Publish"),
        ('a',"Archieved")
    )
    
    title = models.CharField(max_length=200)
    blogger = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # Foreign Key used because post can only have one author/User, but bloggsers can have multiple posts.
    content = models.TextField(max_length=10000, help_text="Enter you blog text here.")
    
    publish_date = models.DateTimeField(blank=True, default=datetime.now())
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)
    slug = models.SlugField(max_length=200, unique=True, blank=True) # how-to-learn-django
    status = models.CharField(max_length=20, choices=STATUS, default='d') 
    #image = models.ImageField(upload_to='blog_pics', default='media/default_post_image.png', blank=True)
    image = models.ImageField(upload_to=user_directory_path, default='default_post_image.png', blank=True)
    # ManyToManyField used because a category can contain many posts. Posts can cover many categories.
    # Category class has already been defined so we can specify the object below.
    category = models.ManyToManyField(Category, help_text='Select  category(ies) for this post')
    
    class Meta:
        ordering = ["-publish_date"] # the newest comes at the top of the list
        #ordering = ["-created_date"]
        #permissions = (("can_mark_archieved", "Set post status as archieved"),)
        
    """ def get_absolute_url(self):
        # Returns the url to access a particular post instance.
        return reverse('post-detail', args=[str(self.id)]) """
    
    def __str__(self):
        return self.title
    
    def display_category(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(category.name for category in self.category.all()[:3])

    display_category.short_description = 'Category(ies)' # this is for the table title in admin panel
    
    # comment count for each post
    def get_comment_count(self):
        comment_count = self.comment_set.all().count() # coomment is the same as Comment class name
        print(comment_count)
        if comment_count > 0 :
            return comment_count
        else:
            return get_random_digit()
    @property
    def get_view_count(self):
        return self.postview_set.all().count()
    
    def get_like_count(self):
        like_count = self.like_set.all().count()
        return like_count
    
    def post_preview(self): ## did not used this one. used {{post.content|truncatechars:20}} instead..
        len_preview=200
        if len(self.content)>len_preview:
            preview_string=self.content[:len_preview] + '...'
        else:
            preview_string=self.content
        return preview_string

    def comments(self):
        return self.comment_set.all()
    
    def categories(self):
        return self.category_set.all()
    
    @property
    def get_last_blog_post(self): ## did not used this one. instaed used the one in the view.
        last_blog_post = self.post_set.order_by('-publish_date').first()
        if last_blog_post:
            return last_blog_post
        return self

class Comment(models.Model):
    """
    Model representing a comment against a blog post.
    """
    commentor = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=1000, help_text="Enter comment about blog here.")

    def __str__(self):
        return self.user.username
    
    class Meta:
        ordering = ["-comment_date"]

    def __str__(self):
        """
        String for representing the Model object.
        """
        len_title=75 # if this is  a long comment first show part of it
        if len(self.content)>len_title:
            titlestring=self.content[:len_title] + '...'
        else:
            titlestring=self.content
        return (f"{self.commentor} - {titlestring} ")
    
    def display_commentor(self):
        """Create a string for the Commentor user. This is required to display Comments in Admin."""
        return self.commentor.username

    display_commentor.short_description = 'Commentor'

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + " " + self.post.title
    
    class Meta:
        ordering = ["-like_date"]

class PostView(models.Model):
    reader = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    view_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reader.username + " " + self.post.title

#in order to handle the contact form
class Contact(models.Model):
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=250)
    email = models.EmailField(max_length=254)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name