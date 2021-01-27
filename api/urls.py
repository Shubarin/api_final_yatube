from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

router = DefaultRouter()
router.register('follow', FollowViewSet, basename='FollowView')
router.register('group', GroupViewSet, basename='GroupView')
router.register(r'posts/(?P<post_id>[^/.]+)/comments', CommentViewSet,
                basename='CommentView')
router.register('posts', PostViewSet, basename='PostView')

urlpatterns = [
    path('', include(router.urls)),
]
