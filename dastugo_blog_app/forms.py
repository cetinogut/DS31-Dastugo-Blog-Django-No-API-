from django import forms
from django.forms import ModelMultipleChoiceField
from django.db.models import fields
from .models import Post, Comment, Category


class PostForm(forms.ModelForm):
    status = forms.ChoiceField(choices=Post.STATUS) # Use the same drop down  from the post model
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                              widget=forms.CheckboxSelectMultiple,
                                              help_text="Choose one or more category") # use all available categories
 
    class Meta:
        model = Post
        fields = (
            'title',
            'category',
            'image',
            'content',
            'status',
            'published_date',
        )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)