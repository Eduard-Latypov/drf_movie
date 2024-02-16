from django_filters import rest_framework as filters

from .models import Movie


class GenreNameFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class MovieFilter(filters.FilterSet):
    genres = GenreNameFilter(field_name="genres__name", lookup_expr="in")
    year = filters.RangeFilter()

    class Meta:
        model = Movie
        fields = ["genres", "year"]
