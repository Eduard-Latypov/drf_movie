from django.urls import path

from . import views

app_name = "movies"


urlpatterns = [
    path("movie/", views.MovieListApiView.as_view()),
    path("movie/<int:pk>/", views.MovieDetailApiView.as_view()),
    path("review/", views.ReviewCreateApiView.as_view()),
    path("rating/", views.AddStarRatingApiView.as_view()),
    path("actors/", views.ActorListApiView.as_view()),
    path("actors/<int:pk>/", views.ActorDetailView.as_view()),
]
