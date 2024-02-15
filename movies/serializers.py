from rest_framework import serializers

from .models import Movie, Review, Rating, Actor


class MovieListSerializer(serializers.ModelSerializer):
    """Список фильмов"""

    rating_user = serializers.BooleanField()
    middle_star = serializers.FloatField()
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Movie
        fields = ["id", "title", "tagline", "category", "rating_user", "middle_star"]


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


class ActorListSerializer(serializers.ModelSerializer):
    """Вывод списка актеров и режиссёров"""

    class Meta:
        model = Actor
        fields = ["id", "name", "image"]


class ActorDetailSerializer(serializers.ModelSerializer):
    """Детальная информация об актере или режиссере"""

    class Meta:
        model = Actor
        fields = "__all__"


class MovieDetailSerializer(serializers.ModelSerializer):
    """Детальная информация о фильме"""

    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    genres = serializers.SlugRelatedField(slug_field="name", many=True, read_only=True)
    directors = ActorListSerializer(many=True, read_only=True)
    actors = ActorListSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ("draft",)
