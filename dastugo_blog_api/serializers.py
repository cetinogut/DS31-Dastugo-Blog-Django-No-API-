from rest_framework import serializers
from dastugo_blog_app.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'image', 'blogger', 'slug', 'category', 'summary', 'content', 'status')
        model = Post