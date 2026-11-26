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
    MovieGenre,
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
        parser.add_argument(
            '--screenings',
            type=int,
            default=120,
            help='Number of screenings to create (default: 120).',
        )
        parser.add_argument(
            '--tickets',
            type=int,
            default=120,
            help='Number of booked seats to create (default: 120).',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        fake = Faker('et_EE')
        Faker.seed(2403)
        random.seed(2403)
        screening_count = options['screenings']
        ticket_count = options['tickets']

        if screening_count < 1:
            raise CommandError('--screenings must be at least 1.')
        if ticket_count < 0:
            raise CommandError('--tickets must not be negative.')

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
                phone_number=f'+372 5{random.randint(1000000, 9999999)}',
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
        MovieGenre.objects.bulk_create(
            [
                MovieGenre(movie=movie, genre=genre)
                for movie in movies
                for genre in fake.random_elements(
                    elements=genres,
                    length=random.randint(1, 3),
                    unique=True,
                )
            ]
        )

        now = timezone.now()
        screenings = []
        screening_seats = {}
        for index in range(screening_count):
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
        ticket_records = []
        for index in range(ticket_count):
            screening = screenings[index % len(screenings)]
            seat_options = screening_seats[screening.pk]
            seat_offset = index // len(screenings)
            seat = seat_options[seat_offset % len(seat_options)]
            status = random.choice(tuple(Booking.Status))
            price = screening.base_price
            bookings.append(Booking(
                user=users[index % len(users)],
                screening=screening,
                status=status,
                total=price,
                created_at=now,
            ))

        Booking.objects.bulk_create(bookings, batch_size=1000)

        for index, booking in enumerate(bookings):
            screening = booking.screening
            seat_options = screening_seats[screening.pk]
            seat_offset = index // len(screenings)
            seat = seat_options[seat_offset % len(seat_options)]
            if booking.status != Booking.Status.CANCELLED:
                ticket_records.append(BookedSeat(
                    booking=booking,
                    screening=screening,
                    seat=seat,
                    price=screening.base_price,
                ))

        BookedSeat.objects.bulk_create(ticket_records, batch_size=1000)

        payments = [
            Payment(
                booking=booking,
                amount=booking.total,
                method=random.choice(('kaart', 'ülekanne', 'mobiilimakse')),
                status=random.choice(('edukas', 'ootel', 'ebaõnnestunud')),
                reference=fake.uuid4(),
                paid_at=now if random.random() < 0.6 else None,
            )
            for booking in bookings
        ]
        Payment.objects.bulk_create(payments, batch_size=1000)

        for _ in range(60):
            Review.objects.create(
                user=random.choice(users),
                movie=random.choice(movies),
                rating=random.randint(1, 5),
                comment=fake.paragraph(nb_sentences=2),
            )

        self.stdout.write(self.style.SUCCESS(
            f'Demoandmed loodud: 40 kasutajat, 3 kino, 9 saali, 864 istekohta, '
            f'20 filmi, 10 žanri, {screening_count} seanssi, {ticket_count} broneeringut, '
            f'{len(ticket_records)} broneeritud kohta, {ticket_count} makset ja 60 arvustust.'
        ))
