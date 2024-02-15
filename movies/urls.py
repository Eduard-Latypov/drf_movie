from django.urls import path

from .views import MovieListApiView, MovieDetailApiView

app_name = "movies"


urlpatterns = [
    path("movie/", MovieListApiView.as_view()),
    path("movie/<int:pk>/", MovieDetailApiView.as_view()),
]
