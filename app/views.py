from django.contrib.auth.models import User
from app.serializers import UserSerializer, BlogPostSerializer
from app.models import BlogPost
from rest_framework import permissions, viewsets, mixins
from django.db.models import Count
from app.permissions import IsOwnerOrReadOnly


class UserViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    """
    retrieve:
    Return the given user.

    list:
    Return a list of all users.
    GET query parameters:
        ordering : string
        values:    'asc', ''
            specifies user ordering by number of posts

    create:
    Create a new user instance.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        ordering = self.request.query_params.get('ordering', '')
        qs = User.objects.annotate(
            posts_count = Count('posts')
        )
        if ordering == 'asc':
            qs = qs.order_by('-posts_count')
        else:
            qs = qs.order_by('posts_count')
        return qs


class BlogPostViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    """
    retrieve:
    Return the given post.

    list:
    Return a list of all posts.
    GET query parameters:
        owner: int
            filter posts list by specific user

    create:
    Create a new post instance.
    """
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def get_queryset(self):
        UID = self.request.query_params.get('owner', None)
        qs = BlogPost.objects.all()
        if UID != None:
            qs = qs.filter(owner__id=int(UID))
        return qs.order_by('-created')

    def get_serializer(self, *args, **kwargs):
        if ('data' in kwargs):
            data = kwargs['data'].copy()
            data['owner'] = self.request.user.pk
            kwargs['data'] = data
        return super(BlogPostViewSet, self).get_serializer(*args, **kwargs)
