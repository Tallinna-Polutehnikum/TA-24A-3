from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from .models import Cinema, CinemaHall, Genre, Movie, MovieGenre, Screening


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
