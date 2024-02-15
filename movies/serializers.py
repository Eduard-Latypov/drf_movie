from rest_framework import serializers

from .models import Movie, Review


class MovieSerializer(serializers.ModelSerializer):
    """Список фильмов"""

    category = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Movie
        fields = ["title", "tagline", "category"]


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Добавление отзыва"""

    class Meta:
        model = Review
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    """Вывод отзыва"""

    class Meta:
        model = Review
        fields = ("text", "name", "parent")


class MovieDetailSerializer(serializers.ModelSerializer):
    """Детальная информация о фильме"""

    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    genres = serializers.SlugRelatedField(slug_field="name", many=True, read_only=True)
    directors = serializers.SlugRelatedField(
        slug_field="name", many=True, read_only=True
    )
    actors = serializers.SlugRelatedField(slug_field="name", many=True, read_only=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ("draft",)

