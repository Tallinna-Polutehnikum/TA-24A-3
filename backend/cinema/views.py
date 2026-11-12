import json
import re
from datetime import date

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods, require_safe

from .models import Cinema, CinemaHall, Movie, Screening

User = get_user_model()
PHONE_PATTERN = re.compile(r'^\+?[0-9 ()-]{7,30}$')


def _json_body(request):
    try:
        body = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return None, JsonResponse({'error': 'Vigane JSON-päring.'}, status=400)
    if not isinstance(body, dict):
        return None, JsonResponse({'error': 'Päringu keha peab olema objekt.'}, status=400)
    return body, None


def _user_data(user):
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'phone_number': user.phone_number,
        'date_of_birth': user.date_of_birth,
        'is_staff': user.is_staff,
    }


def _validation_errors(errors):
    return JsonResponse({'errors': errors}, status=400)


@ensure_csrf_cookie
@require_safe
def csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})


@require_http_methods(['POST'])
def register(request):
    data, error = _json_body(request)
    if error:
        return error

    required = ('username', 'email', 'password', 'phone_number')
    errors = {
        field: 'See väli on kohustuslik.'
        for field in required
        if not str(data.get(field, '')).strip()
    }
    if errors:
        return _validation_errors(errors)

    username = str(data['username']).strip()
    email = str(data['email']).strip().lower()
    phone_number = str(data['phone_number']).strip()
    password = str(data['password'])
    if User.objects.filter(username__iexact=username).exists():
        errors['username'] = 'Selle kasutajanimega konto on juba olemas.'
    if User.objects.filter(email__iexact=email).exists():
        errors['email'] = 'Selle e-postiga konto on juba olemas.'
    try:
        validate_email(email)
    except ValidationError:
        errors['email'] = 'Sisesta korrektne e-posti aadress.'
    if not PHONE_PATTERN.fullmatch(phone_number):
        errors['phone_number'] = 'Sisesta korrektne telefoninumber.'
    if data.get('date_of_birth'):
        parsed_date = parse_date(str(data['date_of_birth']))
        if not parsed_date or parsed_date > date.today():
            errors['date_of_birth'] = 'Sisesta korrektne kuupäev.'
    try:
        validate_password(password, user=User(username=username, email=email))
    except ValidationError as validation_error:
        errors['password'] = list(validation_error.messages)
    if errors:
        return _validation_errors(errors)

    try:
        with transaction.atomic():
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=str(data.get('first_name', '')).strip(),
                last_name=str(data.get('last_name', '')).strip(),
                phone_number=phone_number,
                date_of_birth=data.get('date_of_birth') or None,
            )
    except IntegrityError:
        errors = {}
        if User.objects.filter(username__iexact=username).exists():
            errors['username'] = 'Selle kasutajanimega konto on juba olemas.'
        if User.objects.filter(email__iexact=email).exists():
            errors['email'] = 'Selle e-postiga konto on juba olemas.'
        return _validation_errors(errors or {'detail': 'Konto loomine ebaõnnestus.'})
    login(request, user)
    return JsonResponse({'user': _user_data(user)}, status=201)


@require_http_methods(['POST'])
def user_login(request):
    data, error = _json_body(request)
    if error:
        return error
    username = str(data.get('username', '')).strip()
    password = str(data.get('password', ''))
    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({'error': 'Kasutajanimi või parool on vale.'}, status=400)
    login(request, user)
    return JsonResponse({'user': _user_data(user)})


@require_http_methods(['POST'])
def user_logout(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Kasutaja ei ole sisse logitud.'}, status=401)
    logout(request)
    return JsonResponse({'status': 'ok'})


@require_http_methods(['GET', 'PATCH'])
def me(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Autentimine on vajalik.'}, status=401)
    if request.method == 'GET':
        return JsonResponse({'user': _user_data(request.user)})

    data, error = _json_body(request)
    if error:
        return error
    allowed = {'email', 'first_name', 'last_name', 'phone_number', 'date_of_birth'}
    errors = {}
    unknown = set(data) - allowed
    if unknown:
        return _validation_errors({'detail': 'Profiilis ei saa seda välja muuta.'})
    for field in {'email', 'first_name', 'last_name', 'phone_number'} & set(data):
        if not isinstance(data[field], str):
            errors[field] = 'Sisesta tekst.'
    if 'date_of_birth' in data and data['date_of_birth'] is not None and not isinstance(data['date_of_birth'], str):
        errors['date_of_birth'] = 'Sisesta korrektne kuupäev.'
    if errors:
        return _validation_errors(errors)
    if 'email' in data:
        email = str(data['email']).strip().lower()
        try:
            validate_email(email)
        except ValidationError:
            errors['email'] = 'Sisesta korrektne e-posti aadress.'
        if User.objects.filter(email__iexact=email).exclude(pk=request.user.pk).exists():
            errors['email'] = 'Selle e-postiga konto on juba olemas.'
        data['email'] = email
    if 'phone_number' in data and not PHONE_PATTERN.fullmatch(str(data['phone_number']).strip()):
        errors['phone_number'] = 'Sisesta korrektne telefoninumber.'
    if data.get('date_of_birth'):
        parsed_date = parse_date(data['date_of_birth'])
        if not parsed_date or parsed_date > date.today():
            errors['date_of_birth'] = 'Sisesta korrektne kuupäev.'
    if errors:
        return _validation_errors(errors)
    for field in allowed.intersection(data):
        value = data[field] or None if field == 'date_of_birth' else str(data[field]).strip()
        setattr(request.user, field, value)
    request.user.save(update_fields=list(allowed.intersection(data)))
    return JsonResponse({'user': _user_data(request.user)})


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
