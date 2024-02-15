from django.urls import path

from . import views

app_name = "movies"


urlpatterns = [
    path("movie/", views.MovieListApiView.as_view()),
    path("movie/<int:pk>/", views.MovieDetailApiView.as_view()),
    path("review/", views.ReviewCreateApiView.as_view()),
]
