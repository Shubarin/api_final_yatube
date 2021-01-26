from django_filters import rest_framework as filters

from .models import Post


class GroupFilter(filters.FilterSet):
    group = filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = Post
        fields = ['group', ]
