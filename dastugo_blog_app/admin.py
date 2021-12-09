from django.contrib import admin
from .models import Category, Post, Like, PostView, Comment
#from django.contrib.auth.models import User
from dastugo_user_app.models import Profile

admin.site.register(Category)
#admin.site.register(Post) # see below for alternative admi nregister of this object
admin.site.register(Like)
admin.site.register(PostView)
admin.site.register(Comment)


class CommentsInline(admin.TabularInline): # this is for listing of comments on a post in post detail view in admin panel
    model = Comment
    #fields = ['content']
    extra = 0

class LikesInline(admin.TabularInline): # this is for listing  of likes of a post in post detail view in admin panel
    model = Like
    #fields = ['content']
    extra = 0
    
# Register the Admin classes for Post using the decorator
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'blogger', 'display_category') # listing all posts format in admin site
    list_filter = ('status', 'published_date') # listing all posts, filtering in admin site
    inlines = [CommentsInline]
    #inlines = [LikesInline] # to list both inlines see https://stackoverflow.com/questions/62711269/multiple-inlines-in-model-admin-in-django
    fieldsets = ( # this for post detail and update view in admin site
        ('Post Info', { # section title in admin site
            'fields': ('title', 'blogger', 'category', 'slug')
        }),
        ('Content&Image', { # section title in admin site
            'fields': ('summary', 'content', 'image' )
        }),
        ('Publish Info:', {
            'fields': ('status', 'published_date')
        }),
    )
    
# Define the admin class
class ProfileAdmin(admin.ModelAdmin): # this ca nbe eiather done in user_app admin or here in blog_app admin
    list_display = ('user', 'bio', 'image')

    fields = ['user', 'bio', 'image']
    """ fieldsets = (
        (None, {
            'fields': ('bio')
        }),
        ('Blogger Avatar', {
            'fields': ('image')
        }),
    ) """
# Register the admin class with the associated model
admin.site.register(Profile, ProfileAdmin)