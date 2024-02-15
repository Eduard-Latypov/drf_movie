from rest_framework import serializers

from .models import Movie, Review, Rating


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


class RecursiveSerializer(serializers.Serializer):
    """Вывод рекурсивно children"""

    def to_representation(self, instance):
        serializer = ReviewSerializer(instance=instance, context=self.context)
        return serializer.data


class FilterReviewListSerializer(serializers.ListSerializer):
    """Фильтр комментариев, только parents"""

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class ReviewSerializer(serializers.ModelSerializer):
    """Вывод отзыва"""

    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ["text", "name", "children"]


class CreateRatingSerializer(serializers.ModelSerializer):
    """Добавление рейтинга пользователем"""

    class Meta:
        model = Rating
        fields = ["star", "movie"]

    def create(self, validated_data):
        rating = Rating.objects.update_or_create(
            ip=validated_data.get("ip", None),
            movie=validated_data.get("movie", None),
            defaults={"star": validated_data.get("star")},
        )
        return rating


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
