from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Movie
from .serializers import MovieSerializer, MovieDetailSerializer


class MovieListApiView(APIView):
    """Вывод списка фильмов"""

    def get(self, request):
        movies = Movie.objects.filter(draft=False)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MovieDetailApiView(APIView):
    """Детальная информация о фильме"""

    def get(self, request, pk):
        movie = get_object_or_404(Movie.objects.all(), pk=pk)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)
