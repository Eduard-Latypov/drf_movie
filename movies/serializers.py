from rest_framework import serializers

from .models import Movie


class MovieSerializer(serializers.ModelSerializer):
    """Список фильмов"""

    category = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Movie
        fields = ["title", "tagline", "category"]


class MovieDetailSerializer(serializers.ModelSerializer):
    """Детальная информация о фильме"""

    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    genres = serializers.SlugRelatedField(slug_field="name", many=True, read_only=True)
    directors = serializers.SlugRelatedField(
        slug_field="name", many=True, read_only=True
    )
    actors = serializers.SlugRelatedField(slug_field="name", many=True, read_only=True)

    class Meta:
        model = Movie
        exclude = ("draft",)
