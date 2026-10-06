from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class User(models.Model):
	id = models.BigAutoField(primary_key=True)
	username = models.CharField(max_length=255, db_column='user')
	first_name = models.CharField(max_length=1024)
	last_name = models.CharField(max_length=1024)
	phone_number = models.DecimalField(max_digits=128, decimal_places=0)
	email = models.CharField(max_length=1024)
	date_of_birth = models.DateField(null=True, blank=True)
	password_hash = models.TextField()

	class Meta:
		db_table = 'user'


class Cinema(models.Model):
	id = models.BigAutoField(primary_key=True)
	name = models.CharField(max_length=255, db_column='kino_nimi')
	street_address = models.CharField(max_length=255, db_column='tänava_aadress')
	city = models.CharField(max_length=255, db_column='linn')
	postal_code = models.CharField(max_length=32, db_column='postiindeks')
	country = models.CharField(max_length=255, db_column='riik')

	class Meta:
		db_table = 'kino'


class CinemaHall(models.Model):
	id = models.BigAutoField(primary_key=True)
	cinema = models.ForeignKey(
		Cinema,
		on_delete=models.PROTECT,
		db_column='kino_id',
		related_name='halls',
	)
	name = models.CharField(max_length=50)
	screen_type = models.CharField(max_length=20, db_column='ekraani_tüüp', default='2D')
	capacity = models.PositiveSmallIntegerField(db_column='mahutavus')

	class Meta:
		db_table = 'kinosaalid'


class Seat(models.Model):
	id = models.AutoField(primary_key=True)
	hall = models.ForeignKey(
		CinemaHall,
		on_delete=models.CASCADE,
		db_column='kinosaal_id',
		related_name='seats',
	)
	row = models.CharField(max_length=3, db_column='rida')
	number = models.PositiveSmallIntegerField(db_column='istekoht')

	class Meta:
		db_table = 'istekohad'
		constraints = [
			models.UniqueConstraint(fields=('hall', 'row', 'number'), name='unique_seat_in_hall'),
		]


class Movie(models.Model):
	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=255, db_column='pealkiri', default='')
	description = models.TextField(db_column='kirjeldus', null=True, blank=True)
	duration = models.PositiveSmallIntegerField(db_column='filmi_pikkus', default=0)
	release_date = models.DateField(db_column='väljalaskekuupäev', null=True, blank=True)
	age_rating = models.CharField(max_length=10, db_column='vanusepiirang', null=True, blank=True)
	language = models.CharField(max_length=50, db_column='keel', null=True, blank=True)
	poster_url = models.CharField(max_length=500, db_column='plakati_url', null=True, blank=True)
	trailer_url = models.CharField(max_length=500, db_column='treileri_url', null=True, blank=True)
	is_featured = models.BooleanField(db_column='väikeväärtus', default=False)
	genres = models.ManyToManyField('Genre', through='MovieGenre', related_name='movies')

	class Meta:
		db_table = 'filmid'


class Genre(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50, db_column='nimi')

	class Meta:
		db_table = 'žanrid'


class MovieGenre(models.Model):
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE, db_column='filmi_id')
	genre = models.ForeignKey(Genre, on_delete=models.CASCADE, db_column='žanri_id')

	class Meta:
		db_table = 'filmid_zanrid'
		constraints = [
			models.UniqueConstraint(fields=('movie', 'genre'), name='unique_movie_genre'),
		]


class Screening(models.Model):
	id = models.AutoField(primary_key=True)
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE, db_column='filmi_id', related_name='screenings')
	hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE, db_column='saali_id', related_name='screenings')
	start_time = models.DateTimeField(db_column='algus_aeg')
	end_time = models.DateTimeField(db_column='lopu_aeg')
	language = models.CharField(max_length=50, db_column='keel', null=True, blank=True)
	subtitles = models.CharField(max_length=50, db_column='subtiitrid', null=True, blank=True)
	base_price = models.DecimalField(max_digits=8, decimal_places=2, db_column='alghind')

	class Meta:
		db_table = 'seansid'
		constraints = [
			models.CheckConstraint(condition=models.Q(end_time__gt=models.F('start_time')), name='screening_end_after_start'),
		]


class Booking(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='kasutaja_id', related_name='bookings')
	screening = models.ForeignKey(Screening, on_delete=models.CASCADE, db_column='seansi_id', related_name='bookings')
	status = models.CharField(max_length=20, db_column='staatus', default='ootel')
	total = models.DecimalField(max_digits=8, decimal_places=2, db_column='kogusumma')
	created_at = models.DateTimeField(db_column='loodud', auto_now_add=True)

	class Meta:
		db_table = 'broneeringud'


class BookedSeat(models.Model):
	id = models.AutoField(primary_key=True)
	booking = models.ForeignKey(Booking, on_delete=models.CASCADE, db_column='broneeringu_id', related_name='booked_seats')
	screening = models.ForeignKey(Screening, on_delete=models.CASCADE, db_column='seansi_id', related_name='booked_seats')
	seat = models.ForeignKey(Seat, on_delete=models.CASCADE, db_column='istekoha_id', related_name='bookings')
	price = models.DecimalField(max_digits=8, decimal_places=2, db_column='hind')

	class Meta:
		db_table = 'broneeritud_kohad'
		constraints = [
			models.UniqueConstraint(fields=('screening', 'seat'), name='unique_booked_seat_per_screening'),
		]


class Payment(models.Model):
	id = models.AutoField(primary_key=True)
	booking = models.ForeignKey(Booking, on_delete=models.CASCADE, db_column='broneeringu_id', related_name='payments')
	amount = models.DecimalField(max_digits=8, decimal_places=2, db_column='summa')
	method = models.CharField(max_length=30, db_column='makseviis')
	status = models.CharField(max_length=20, db_column='staatus')
	reference = models.CharField(max_length=255, db_column='makse_viide', null=True, blank=True)
	paid_at = models.DateTimeField(db_column='makstud', null=True, blank=True)

	class Meta:
		db_table = 'maksed'


class Review(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='kasutaja_id', related_name='reviews')
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE, db_column='filmi_id', related_name='reviews')
	rating = models.PositiveSmallIntegerField(
		db_column='hinnang',
		null=True,
		blank=True,
		validators=[MinValueValidator(1), MaxValueValidator(5)],
	)
	comment = models.TextField(db_column='kommentaar', null=True, blank=True)
	created_at = models.DateTimeField(db_column='loodud', auto_now_add=True)

	class Meta:
		db_table = 'arvustused'