from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_safe

from .models import Cinema, CinemaHall, Movie, Screening


def health(request):
    return JsonResponse({
        'app': 'cinema',
        'status': 'ok',
    })


def _movie_data(movie):
    return {
        'id': movie.id,
        'title': movie.title,
        'description': movie.description,
        'duration': movie.duration,
        'release_date': movie.release_date,
        'age_rating': movie.age_rating,
        'language': movie.language,
        'poster_url': movie.poster_url,
        'trailer_url': movie.trailer_url,
        'is_featured': movie.is_featured,
        'genres': [
            {'id': genre.id, 'name': genre.name}
            for genre in movie.genres.all()
        ],
    }


def _cinema_data(cinema):
    return {
        'id': cinema.id,
        'name': cinema.name,
        'street_address': cinema.street_address,
        'city': cinema.city,
        'postal_code': cinema.postal_code,
        'country': cinema.country,
    }


def _hall_data(hall):
    return {
        'id': hall.id,
        'cinema_id': hall.cinema_id,
        'cinema_name': hall.cinema.name,
        'name': hall.name,
        'screen_type': hall.screen_type,
        'capacity': hall.capacity,
    }


def _screening_data(screening):
    return {
        'id': screening.id,
        'movie_id': screening.movie_id,
        'movie_title': screening.movie.title,
        'hall_id': screening.hall_id,
        'hall_name': screening.hall.name,
        'screen_type': screening.hall.screen_type,
        'cinema_id': screening.hall.cinema_id,
        'cinema_name': screening.hall.cinema.name,
        'start_time': screening.start_time,
        'end_time': screening.end_time,
        'language': screening.language,
        'subtitles': screening.subtitles,
        'base_price': screening.base_price,
    }


@require_safe
def movies(request):
    results = Movie.objects.prefetch_related('genres').order_by('id')
    return JsonResponse({'results': [_movie_data(movie) for movie in results]})


@require_safe
def movie_detail(request, movie_id):
    movie = get_object_or_404(
        Movie.objects.prefetch_related('genres'),
        pk=movie_id,
    )
    return JsonResponse(_movie_data(movie))


@require_safe
def cinemas(request):
    results = Cinema.objects.order_by('id')
    return JsonResponse({'results': [_cinema_data(cinema) for cinema in results]})


@require_safe
def cinema_detail(request, cinema_id):
    cinema = get_object_or_404(Cinema, pk=cinema_id)
    return JsonResponse(_cinema_data(cinema))


@require_safe
def halls(request):
    results = CinemaHall.objects.select_related('cinema').order_by('id')
    return JsonResponse({'results': [_hall_data(hall) for hall in results]})


@require_safe
def hall_detail(request, hall_id):
    hall = get_object_or_404(
        CinemaHall.objects.select_related('cinema'),
        pk=hall_id,
    )
    return JsonResponse(_hall_data(hall))


@require_safe
def screenings(request):
    results = Screening.objects.select_related(
        'movie',
        'hall__cinema',
    ).order_by('start_time', 'id')
    return JsonResponse({
        'results': [_screening_data(screening) for screening in results],
    })


@require_safe
def screening_detail(request, screening_id):
    screening = get_object_or_404(
        Screening.objects.select_related('movie', 'hall__cinema'),
        pk=screening_id,
    )
    return JsonResponse(_screening_data(screening))
