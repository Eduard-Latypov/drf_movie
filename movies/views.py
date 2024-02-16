from django.db import models
from rest_framework import status, permissions
from rest_framework import generics

from django_filters.rest_framework import DjangoFilterBackend

from .models import Movie, Review, Actor
from .serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    ReviewCreateSerializer,
    CreateRatingSerializer,
    ActorListSerializer,
    ActorDetailSerializer,
)
from .utils import get_client_ip
from .filters import MovieFilter


class MovieListApiView(generics.ListAPIView):
    """Вывод списка фильмов"""

    serializer_class = MovieListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MovieFilter
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        movies = (
            Movie.objects.prefetch_related("ratings")
            .filter(draft=False)
            .annotate(
                rating_user=models.Count(
                    "ratings", filter=models.Q(ratings__ip=get_client_ip(self.request))
                )
            )
            .annotate(middle_star=models.Sum("ratings__star") / models.Count("ratings"))
        )
        return movies


class MovieDetailApiView(generics.RetrieveAPIView):
    """Детальная информация о фильме"""

    queryset = Movie.objects.prefetch_related(
        "genres", "actors", "directors", "category", "reviews"
    )
    serializer_class = MovieDetailSerializer


class ReviewCreateApiView(generics.CreateAPIView):
    """Добавление отзыва к фильму"""

    serializer_class = ReviewCreateSerializer


class AddStarRatingApiView(generics.CreateAPIView):
    """Добавление звезды к фильму"""

    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorListApiView(generics.ListAPIView):
    """Вывод списка актеров и режиссеров"""

    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorDetailView(generics.RetrieveAPIView):
    """Вывод полного описания актера или режиссера"""

    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
