from django.urls import path

from . import views

app_name = 'cinema'

urlpatterns = [
    path('', views.health, name='health'),
    path('movies/', views.movies, name='movies'),
    path('movies/<int:movie_id>/', views.movie_detail, name='movie-detail'),
    path('cinemas/', views.cinemas, name='cinemas'),
    path('cinemas/<int:cinema_id>/', views.cinema_detail, name='cinema-detail'),
    path('halls/', views.halls, name='halls'),
    path('halls/<int:hall_id>/', views.hall_detail, name='hall-detail'),
    path('screenings/', views.screenings, name='screenings'),
    path(
        'screenings/<int:screening_id>/',
        views.screening_detail,
        name='screening-detail',
    ),
]
