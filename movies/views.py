from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Movie, Review
from .serializers import (
    MovieSerializer,
    MovieDetailSerializer,
    ReviewCreateSerializer,
    CreateRatingSerializer,
)
from .utils import get_client_ip


class MovieListApiView(APIView):
    """Вывод списка фильмов"""

    def get(self, request):
        movies = Movie.objects.filter(draft=False)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)


class MovieDetailApiView(APIView):
    """Детальная информация о фильме"""

    def get(self, request, pk):
        movie = get_object_or_404(Movie.objects.all(), pk=pk)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)


class ReviewCreateApiView(APIView):
    """Добавление отзыва к фильму"""

    def post(self, request):
        serializer = ReviewCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddStarRatingApiView(APIView):
    """Добавление звезды к фильму"""

    def post(self, request):
        ip = get_client_ip(request)
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=ip)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
