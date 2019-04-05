from django.contrib.auth.models import User, Group
from rest_framework import serializers
from app.models import BlogPost


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    User serializer
    """
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        """
        User creation method, added seting user password
        """
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    posts_count = serializers.SerializerMethodField()

    def get_posts_count(self, obj):
        """
        Gets number of posts of user
        """
        return obj.posts.count()

    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'password', 'posts_count')


class BlogPostSerializer(serializers.ModelSerializer):
    """
    Blog post serializer
    """
    class Meta:
        model = BlogPost
        fields = ('id', 'created', 'title', 'body', 'owner')
