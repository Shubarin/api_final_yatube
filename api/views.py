from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api.filters import GroupFilter
from api.models import Comment, Follow, Group, Post, User
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (CommentSerializer, FollowSerializer,
                             GroupSerializer, PostSerializer)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def list(self, request, post_id=None):
        post = get_object_or_404(Post, pk=post_id)
        queryset = post.comments.all()
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        username = request.user.username
        if self.request.query_params.get('search'):
            queryset = get_list_or_404(Follow, user__username=username)
        else:
            queryset = get_list_or_404(Follow, following__username=username)
        serializer = FollowSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        if not self.request.data.get('following'):
            raise ValidationError('Вы забыли указать автора для подписки')
        following = get_object_or_404(User, username=self.request.data.get(
            'following'))
        if following == self.request.user:
            raise ValidationError('Нельзя подписаться на себя')
        follow = self.request.user.user.filter(following=following).count()
        if follow:
            raise ValidationError('Нельзя подписаться на автора дважды')
        serializer.save(user=self.request.user, following=following)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        if not request.data.get('title'):
            return Response('Плохой запрос', status=status.HTTP_400_BAD_REQUEST)
        queryset = Group.objects.create(title=request.data.get('title'))
        serializer = GroupSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_class = GroupFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
