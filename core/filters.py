from django.db.models import Q
from django_filters import rest_framework as filters

from core import models

LIKE = 'unaccent__icontains' # Usando unaccent para ignorar acentos e trazer palavras semelhantes
ICONTAINS = 'icontains'
LIKE_IN = 'incontains'  # Usando unaccent para ignorar acentos em listas
UNACCENT_IEXACT = 'unaccent__iexact'
EQUALS = 'exact'
STARTS_WITH = 'startswith'
GT = 'gt'
LT = 'lt'
GTE = 'gte'
LTE = 'lte'
IN = 'in'

class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass

class LostItemFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr=LIKE)
    last_seen_details = filters.CharFilter(lookup_expr=LIKE)
    city = filters.CharFilter(lookup_expr=LIKE)
    category_name = filters.CharFilter(field_name='category__name', lookup_expr=LIKE)
    user = filters.NumberFilter(field_name='user', lookup_expr=EQUALS)

    search = filters.CharFilter(method='filter_search')

    @staticmethod
    def filter_search(queryset, name, value):
        """
        Custom filter to search across multiple fields.
        """
        return queryset.filter(
            Q(title__unaccent__icontains=value) |
            Q(last_seen_details__unaccent__icontains=value) |
            Q(city__unaccent__icontains=value) |
            Q(category__name__unaccent__icontains=value)
        )

    class Meta:
        model = models.LostItem
        fields = ['last_seen_details', 'title', 'category_name', 'city', 'user']


class FoundItemFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr=LIKE)
    description = filters.CharFilter(lookup_expr=LIKE)
    category_name = filters.CharFilter(field_name='category__name', lookup_expr=LIKE)
    city = filters.CharFilter(lookup_expr=LIKE)
    user = filters.NumberFilter(field_name='user', lookup_expr=EQUALS)

    class Meta:
        model = models.FoundItem
        fields = ['title', 'description', 'category_name', 'city', 'user']


class CategoryFilter(filters.FilterSet):
    items = filters.CharFilter(lookup_expr=LIKE)

    class Meta:
        model = models.Category
        fields = ['items']


class CommentFilter(filters.FilterSet):
    found_item = filters.NumberFilter(lookup_expr=EQUALS)
    lost_item = filters.NumberFilter(lookup_expr=EQUALS)
    comment = filters.NumberFilter(lookup_expr=EQUALS)
    not_comment = filters.BooleanFilter(field_name='comment', lookup_expr='isnull')

    class Meta:
        model = models.Comment
        fields = ['found_item', 'lost_item', 'comment', 'not_comment']
