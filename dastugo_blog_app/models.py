from django.db import models
from datetime import date
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User #Blog author or commenter


# def user_directory_path(instance, filename):
#     return 'blog/{0}/{1}'.format(instance.author.id, filename)


class Category(models.Model):
    """
    Model representing a post category. Each post can have more than one category
    """
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

STATUS = (
    ('d',"Draft"),
    ('p',"Publish"),
    ('a',"Archieved")
)

class Post(models.Model):
    """
    Model representing a blog post.
    """
    title = models.CharField(max_length=200)
    blogger = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # Foreign Key used because post can only have one author/User, but bloggsers can have multiple posts.
    content = models.TextField(max_length=10000, help_text="Enter you blog text here.")
    published_date = models.DateField(default=date.today)
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)
    slug = models.SlugField(max_length=200, unique=True) # how-to-learn-django
    status = models.IntegerField(choices=STATUS, default=0) 
    image = models.ImageField(upload_to='blog_pics', default='media/default_post_image.png', blank=True)
    
    # ManyToManyField used because a category can contain many posts. Posts can cover many categories.
    # Category class has already been defined so we can specify the object above.
    category = models.ManyToManyField(Category, help_text='Select a category for this post')
    
    class Meta:
        ordering = ["-published_date"]
        #ordering = ["-created_date"]
        #permissions = (("can_mark_archieved", "Set post status as archieved"),)
        
    def get_absolute_url(self):
        """
        Returns the url to access a particular post instance.
        """
        return reverse('post-detail', args=[str(self.id)])
    
    def __str__(self):
        return self.title
    
    def display_category(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(category.name for category in self.category.all()[:3])

    display_category.short_description = 'Category(ies)' # this is for the table title in admin panel
    
    # comment count for each post
    def get_comment_count(self):
        comment_count = self.comment_set.all().count()
        return comment_count
    
    def get_like_count(self):
        like_count = self.like_set.all().count()
        return like_count
    
    def post_preview(self):
        len_preview=200
        if len(self.content)>len_preview:
            preview_string=self.content[:len_preview] + '...'
        else:
            preview_string=self.content
        return preview_string

    def comments(self):
        return self.comment_set.all()


# class Comment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     time_stamp = models.DateTimeField(auto_now_add=True)
#     content = models.TextField()

#     def __str__(self):
#         return self.user.username


# class Like(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.user.username


# class PostView(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     time_stamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.user.username