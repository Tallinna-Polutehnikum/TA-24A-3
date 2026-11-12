from django.test import Client, SimpleTestCase, TestCase
from django.urls import reverse

from .models import Cinema, CinemaHall, Genre, Movie, MovieGenre, Screening, User


class HealthViewTests(SimpleTestCase):
    def test_health_endpoint_returns_app_status(self):
        response = self.client.get(reverse('cinema:health'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'app': 'cinema',
            'status': 'ok',
        })


class CatalogueEndpointTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cinema = Cinema.objects.create(
            name='Test Cinema',
            street_address='Main Street 1',
            city='Tallinn',
            postal_code='10111',
            country='Eesti',
        )
        cls.hall = CinemaHall.objects.create(
            cinema=cls.cinema,
            name='Hall 1',
            screen_type='2D',
            capacity=100,
        )
        cls.movie = Movie.objects.create(
            title='Test Movie',
            duration=100,
            language='eesti',
            is_featured=True,
        )
        cls.genre = Genre.objects.create(name='Draama')
        MovieGenre.objects.create(movie=cls.movie, genre=cls.genre)
        cls.screening = Screening.objects.create(
            movie=cls.movie,
            hall=cls.hall,
            start_time='2026-10-13T12:00:00Z',
            end_time='2026-10-13T13:40:00Z',
            base_price='12.50',
        )

    def test_movie_list_includes_genres(self):
        response = self.client.get(reverse('cinema:movies'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['results'][0]['genres'], [
            {'id': self.genre.id, 'name': 'Draama'},
        ])

    def test_cinema_hall_and_screening_lists_include_public_fields(self):
        cinema_response = self.client.get(reverse('cinema:cinemas'))
        hall_response = self.client.get(reverse('cinema:halls'))
        screening_response = self.client.get(reverse('cinema:screenings'))

        self.assertEqual(cinema_response.status_code, 200)
        self.assertEqual(cinema_response.json()['results'][0]['name'], 'Test Cinema')
        self.assertEqual(hall_response.status_code, 200)
        self.assertEqual(hall_response.json()['results'][0]['cinema_name'], 'Test Cinema')
        self.assertEqual(screening_response.status_code, 200)
        self.assertEqual(
            screening_response.json()['results'][0]['movie_title'],
            'Test Movie',
        )
        self.assertEqual(
            screening_response.json()['results'][0]['base_price'],
            '12.50',
        )
        self.assertEqual(
            screening_response.json()['results'][0]['screen_type'],
            '2D',
        )
        self.assertEqual(
            screening_response.json()['results'][0]['screen_type'],
            '2D',
        )

    def test_detail_endpoints_return_the_requested_resources(self):
        responses = (
            self.client.get(reverse('cinema:movie-detail', args=[self.movie.id])),
            self.client.get(reverse('cinema:cinema-detail', args=[self.cinema.id])),
            self.client.get(reverse('cinema:hall-detail', args=[self.hall.id])),
            self.client.get(
                reverse('cinema:screening-detail', args=[self.screening.id]),
            ),
        )

        self.assertTrue(all(response.status_code == 200 for response in responses))
        self.assertEqual(responses[0].json()['title'], 'Test Movie')
        self.assertEqual(responses[1].json()['name'], 'Test Cinema')
        self.assertEqual(responses[2].json()['cinema_name'], 'Test Cinema')
        self.assertEqual(responses[3].json()['movie_title'], 'Test Movie')

    def test_detail_endpoint_returns_404_for_unknown_movie(self):
        response = self.client.get(
            reverse('cinema:movie-detail', args=[self.movie.id + 1]),
        )

        self.assertEqual(response.status_code, 404)

    def test_catalogue_endpoints_reject_write_requests(self):
        response = self.client.post(reverse('cinema:movies'))

        self.assertEqual(response.status_code, 405)


class AuthenticationEndpointTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        csrf_response = self.client.get(reverse('cinema:auth-csrf'))
        self.csrf_token = csrf_response.cookies['csrftoken'].value
        self.user = User.objects.create_user(
            username='existing',
            email='existing@example.test',
            password='CorrectPass123!',
            phone_number='+372 5555 5555',
        )

    def post_json(self, url, data):
        return self.client.post(
            url,
            data=data,
            content_type='application/json',
            HTTP_X_CSRFTOKEN=self.csrf_token,
        )

    def test_registration_hashes_password_and_logs_user_in(self):
        response = self.post_json(
            reverse('cinema:auth-register'),
            {
                'username': 'new-user',
                'email': 'new@example.test',
                'password': 'CorrectPass123!',
                'phone_number': '+372 5555 4444',
            },
        )

        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username='new-user')
        self.assertNotEqual(user.password, 'CorrectPass123!')
        self.assertTrue(user.check_password('CorrectPass123!'))
        self.assertEqual(response.json()['user']['email'], 'new@example.test')

    def test_duplicate_user_and_invalid_login_return_clear_errors(self):
        duplicate = self.post_json(
            reverse('cinema:auth-register'),
            {
                'username': 'existing',
                'email': 'another@example.test',
                'password': 'CorrectPass123!',
                'phone_number': '+372 5555 4444',
            },
        )
        login_response = self.post_json(
            reverse('cinema:auth-login'),
            {'username': 'existing', 'password': 'wrong'},
        )

        self.assertEqual(duplicate.status_code, 400)
        self.assertIn('username', duplicate.json()['errors'])

        duplicate_email = self.post_json(
            reverse('cinema:auth-register'),
            {
                'username': 'another-user',
                'email': 'existing@example.test',
                'password': 'CorrectPass123!',
                'phone_number': '+372 5555 4444',
            },
        )
        self.assertEqual(login_response.status_code, 400)
        self.assertIn('vale', login_response.json()['error'])
        self.assertEqual(duplicate_email.status_code, 400)
        self.assertIn('email', duplicate_email.json()['errors'])

    def test_me_only_returns_and_updates_current_user(self):
        self.client.force_login(self.user)
        other = User.objects.create_user(
            username='other',
            email='other@example.test',
            password='CorrectPass123!',
            phone_number='+372 5555 6666',
        )

        response = self.client.get(reverse('cinema:auth-me'))
        update = self.client.patch(
            reverse('cinema:auth-me'),
            data={'first_name': 'Uus nimi', 'email': 'updated@example.test'},
            content_type='application/json',
            HTTP_X_CSRFTOKEN=self.csrf_token,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['user']['id'], self.user.id)
        self.assertNotIn('password', response.json()['user'])
        self.assertNotEqual(response.json()['user']['username'], other.username)
        self.assertEqual(update.status_code, 200)
        self.assertEqual(update.json()['user']['email'], 'updated@example.test')
        self.assertEqual(User.objects.get(pk=self.user.pk).first_name, 'Uus nimi')

    def test_logout_ends_session(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('cinema:auth-logout'),
            HTTP_X_CSRFTOKEN=self.csrf_token,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            self.client.get(reverse('cinema:auth-me')).status_code,
            401,
        )

    def test_profile_rejects_non_string_and_future_dates(self):
        self.client.force_login(self.user)

        invalid_type = self.client.patch(
            reverse('cinema:auth-me'),
            data={'first_name': {'unexpected': 'object'}},
            content_type='application/json',
            HTTP_X_CSRFTOKEN=self.csrf_token,
        )
        future_date = self.client.patch(
            reverse('cinema:auth-me'),
            data={'date_of_birth': '2999-01-01'},
            content_type='application/json',
            HTTP_X_CSRFTOKEN=self.csrf_token,
        )

        self.assertEqual(invalid_type.status_code, 400)
        self.assertIn('first_name', invalid_type.json()['errors'])
        self.assertEqual(future_date.status_code, 400)
        self.assertIn('date_of_birth', future_date.json()['errors'])

    def test_authentication_requests_require_csrf(self):
        response = Client(enforce_csrf_checks=True).post(
            reverse('cinema:auth-login'),
            data={'username': 'existing', 'password': 'CorrectPass123!'},
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 403)
