from django.db import models


class User(models.Model):
    username = models.CharField(max_length=255, unique=True, db_column='user')
    first_name = models.CharField(max_length=1024)
    last_name = models.CharField(max_length=1024)
    phone_number = models.CharField(max_length=30)
    email = models.EmailField(max_length=1024, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    password_hash = models.TextField()

    class Meta:
        db_table = 'user'


class Cinema(models.Model):
    name = models.CharField(max_length=255, db_column='kino_nimi')
    street_address = models.CharField(max_length=255, db_column='tänava_aadress')
    city = models.CharField(max_length=255, db_column='linn')
    postal_code = models.CharField(max_length=32, db_column='postiindeks')
    country = models.CharField(max_length=255, db_column='riik')

    class Meta:
        db_table = 'kino'


class Auditorium(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.PROTECT, db_column='kino_id')
    name = models.CharField(max_length=50)
    screen_type = models.CharField(max_length=20, default='2D', db_column='ekraani_tüüp')
    capacity = models.PositiveSmallIntegerField(db_column='mahutavus')

    class Meta:
        db_table = 'kinosaalid'


class Seat(models.Model):
    auditorium = models.ForeignKey(Auditorium, on_delete=models.CASCADE, db_column='saali_id')
    row = models.CharField(max_length=3, db_column='rida')
    number = models.PositiveSmallIntegerField(db_column='istekoht')

    class Meta:
        db_table = 'istekohad'
        constraints = [
            models.UniqueConstraint(
                fields=('auditorium', 'row', 'number'),
                name='istekoht_saali_rea_num_uniq',
            ),
        ]


class Movie(models.Model):
    title = models.CharField(max_length=255, db_column='pealkiri')
    description = models.TextField(null=True, blank=True, db_column='kirjeldus')
    duration_minutes = models.PositiveSmallIntegerField(default=0, db_column='filmi_pikkus')
    release_date = models.DateField(null=True, blank=True, db_column='väljalaskekuupäev')
    age_rating = models.CharField(max_length=10, null=True, blank=True, db_column='vanusepiirang')
    language = models.CharField(max_length=50, null=True, blank=True, db_column='keel')
    poster_url = models.CharField(max_length=500, null=True, blank=True, db_column='plakati_url')
    trailer_url = models.CharField(max_length=500, null=True, blank=True, db_column='treileri_url')
    is_small_value = models.BooleanField(default=False, db_column='väikeväärtus')

    class Meta:
        db_table = 'filmid'


class Genre(models.Model):
    name = models.CharField(max_length=50, db_column='nimi')

    class Meta:
        db_table = 'žanrid'


class Screening(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT, db_column='filmi_id')
    auditorium = models.ForeignKey(Auditorium, on_delete=models.PROTECT, db_column='saali_id')
    starts_at = models.DateTimeField(db_column='algus_aeg')
    ends_at = models.DateTimeField(db_column='lopu_aeg')
    language = models.CharField(max_length=50, null=True, blank=True, db_column='keel')
    subtitles = models.CharField(max_length=50, null=True, blank=True, db_column='subtiitrid')
    price = models.DecimalField(max_digits=8, decimal_places=2, db_column='alghind')

    class Meta:
        db_table = 'seansid'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(ends_at__gt=models.F('starts_at')),
                name='seans_lopp_parast_algust',
            ),
        ]


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, db_column='kasutaja_id')
    screening = models.ForeignKey(Screening, on_delete=models.PROTECT, db_column='seansi_id')
    status = models.CharField(max_length=20, default='ootel', db_column='staatus')
    total = models.DecimalField(max_digits=8, decimal_places=2, db_column='kogusumma')
    created_at = models.DateTimeField(auto_now_add=True, db_column='loodud')

    class Meta:
        db_table = 'broneeringud'


class ReservedSeat(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, db_column='broneeringu_id')
    screening = models.ForeignKey(Screening, on_delete=models.PROTECT, db_column='seansi_id')
    seat = models.ForeignKey(Seat, on_delete=models.PROTECT, db_column='istekoha_id')
    price = models.DecimalField(max_digits=8, decimal_places=2, db_column='hind')

    class Meta:
        db_table = 'broneeritud_kohad'
        constraints = [
            models.UniqueConstraint(
                fields=('screening', 'seat'),
                name='broneeritud_seans_iste_uniq',
            ),
        ]


class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, db_column='broneeringu_id')
    amount = models.DecimalField(max_digits=8, decimal_places=2, db_column='summa')
    method = models.CharField(max_length=30, db_column='makseviis')
    status = models.CharField(max_length=20, db_column='staatus')
    reference = models.CharField(max_length=255, null=True, blank=True, db_column='makse_viide')
    paid_at = models.DateTimeField(null=True, blank=True, db_column='makstud')

    class Meta:
        db_table = 'maksed'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, db_column='kasutaja_id')
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT, db_column='filmi_id')
    rating = models.PositiveSmallIntegerField(null=True, blank=True, db_column='hinnang')
    comment = models.TextField(null=True, blank=True, db_column='kommentaar')
    created_at = models.DateTimeField(auto_now_add=True, db_column='loodud')

    class Meta:
        db_table = 'arvustused'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(rating__isnull=True) | models.Q(rating__gte=1, rating__lte=5),
                name='arvustus_hinnang_1_5',
            ),
        ]
