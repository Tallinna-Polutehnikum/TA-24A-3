import random
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from faker import Faker

from cinema.models import (
    Booking,
    BookedSeat,
    Cinema,
    CinemaHall,
    Genre,
    Movie,
    Payment,
    Review,
    Screening,
    Seat,
    User,
)


class Command(BaseCommand):
    help = 'Create linked cinema demo data using Faker.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete existing cinema data before creating demo data.',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        fake = Faker('et_EE')
        Faker.seed(2403)
        random.seed(2403)

        if not options['clear'] and any(
            model.objects.exists()
            for model in (User, Cinema, CinemaHall, Seat, Movie, Genre, Screening, Booking)
        ):
            raise CommandError(
                'Kinoandmebaas pole tühi. Olemasolevate andmete asendamiseks käivita käsuga --clear.'
            )

        if options['clear']:
            for model in (BookedSeat, Payment, Review, Booking, Screening, Seat, Genre,
                          Movie, CinemaHall, User, Cinema):
                model.objects.all().delete()

        users = [
            User.objects.create(
                username=f'demo_{index:03}',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone_number=fake.phone_number()[:30],
                email=f'demo{index:03}@example.test',
                date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=75),
                password_hash=make_password('DemoPass123!'),
            )
            for index in range(1, 41)
        ]
        cinemas = [
            Cinema.objects.create(
                name=f'{fake.city()} Kino {index}',
                street_address=fake.street_address(),
                city=fake.city(),
                postal_code=fake.postcode()[:32],
                country='Eesti',
            )
            for index in range(1, 4)
        ]

        halls = []
        seats_by_hall = {}
        for cinema in cinemas:
            for hall_number in range(1, 4):
                hall = CinemaHall.objects.create(
                    cinema=cinema,
                    name=f'Saal {hall_number}',
                    screen_type=random.choice(('2D', '3D', 'IMAX')),
                    capacity=96,
                )
                halls.append(hall)
                seats = [
                    Seat(hall=hall, row=chr(65 + row), number=number)
                    for row in range(8)
                    for number in range(1, 13)
                ]
                Seat.objects.bulk_create(seats)
                seats_by_hall[hall.pk] = seats

        genres = [
            Genre.objects.create(name=name)
            for name in (
                'Draama', 'Komöödia', 'Põnevik', 'Ulme', 'Seiklus',
                'Animatsioon', 'Krimi', 'Romantika', 'Õudus', 'Dokumentaal',
            )
        ]
        movies = [
            Movie.objects.create(
                title=fake.catch_phrase()[:255],
                description=fake.paragraph(nb_sentences=3),
                duration=random.randint(80, 180),
                release_date=fake.date_between(start_date='-8y', end_date='today'),
                age_rating=random.choice(('Perefilm', 'MS-12', 'K-14', 'K-16')),
                language=random.choice(('eesti', 'inglise', 'soome')),
                is_featured=random.choice((True, False)),
            )
            for _ in range(20)
        ]

        now = timezone.now()
        screenings = []
        screening_seats = {}
        for index in range(120):
            hall = halls[index % len(halls)]
            movie = movies[index % len(movies)]
            starts_at = now + timedelta(
                days=random.randint(-20, 30),
                hours=random.choice((10, 13, 16, 19, 21)),
            )
            screening = Screening.objects.create(
                movie=movie,
                hall=hall,
                start_time=starts_at,
                end_time=starts_at + timedelta(minutes=movie.duration + 15),
                language=movie.language,
                subtitles=random.choice(('eesti', 'inglise', None)),
                base_price=Decimal(random.randrange(700, 1601)) / 100,
            )
            screenings.append(screening)
            screening_seats[screening.pk] = seats_by_hall[hall.pk]

        bookings = []
        booked_seats = set()
        for index, screening in enumerate(screenings):
            seat_options = screening_seats[screening.pk]
            seat_count = random.randint(1, 3)
            seats = random.sample(seat_options, seat_count)
            price = screening.base_price
            booking = Booking.objects.create(
                user=users[index % len(users)],
                screening=screening,
                status=random.choice(('ootel', 'kinnitatud', 'tühistatud')),
                total=price * seat_count,
            )
            bookings.append(booking)
            for seat in seats:
                BookedSeat.objects.create(
                    booking=booking,
                    screening=screening,
                    seat=seat,
                    price=price,
                )
                booked_seats.add((screening.pk, seat.pk))

        for booking in bookings:
            payment_status = random.choice(('edukas', 'ootel', 'ebaõnnestunud'))
            Payment.objects.create(
                booking=booking,
                amount=booking.total,
                method=random.choice(('kaart', 'ülekanne', 'mobiilimakse')),
                status=payment_status,
                reference=fake.uuid4(),
                paid_at=now if payment_status == 'edukas' else None,
            )

        for _ in range(60):
            Review.objects.create(
                user=random.choice(users),
                movie=random.choice(movies),
                rating=random.randint(1, 5),
                comment=fake.paragraph(nb_sentences=2),
            )

        self.stdout.write(self.style.SUCCESS(
            'Demoandmed loodud: 40 kasutajat, 3 kino, 9 saali, 864 istekohta, '
            '20 filmi, 10 žanri, 120 seanssi, 120 broneeringut, '
            f'{len(booked_seats)} broneeritud kohta, 120 makset ja 60 arvustust.'
        ))
