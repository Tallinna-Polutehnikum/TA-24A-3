from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Cinema',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='kino_nimi', max_length=255)),
                ('street_address', models.CharField(db_column='tänava_aadress', max_length=255)),
                ('city', models.CharField(db_column='linn', max_length=255)),
                ('postal_code', models.CharField(db_column='postiindeks', max_length=32)),
                ('country', models.CharField(db_column='riik', max_length=255)),
            ],
            options={'db_table': 'kino'},
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='nimi', max_length=50)),
            ],
            options={'db_table': 'žanrid'},
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(db_column='pealkiri', default='', max_length=255)),
                ('description', models.TextField(blank=True, db_column='kirjeldus', null=True)),
                ('duration', models.PositiveSmallIntegerField(db_column='filmi_pikkus', default=0)),
                ('release_date', models.DateField(blank=True, db_column='väljalaskekuupäev', null=True)),
                ('age_rating', models.CharField(blank=True, db_column='vanusepiirang', max_length=10, null=True)),
                ('language', models.CharField(blank=True, db_column='keel', max_length=50, null=True)),
                ('poster_url', models.CharField(blank=True, db_column='plakati_url', max_length=500, null=True)),
                ('trailer_url', models.CharField(blank=True, db_column='treileri_url', max_length=500, null=True)),
                ('is_featured', models.BooleanField(db_column='väikeväärtus', default=False)),
            ],
            options={'db_table': 'filmid'},
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(db_column='user', max_length=255)),
                ('first_name', models.CharField(max_length=1024)),
                ('last_name', models.CharField(max_length=1024)),
                ('phone_number', models.DecimalField(decimal_places=0, max_digits=128)),
                ('email', models.CharField(max_length=1024)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('password_hash', models.TextField()),
            ],
            options={'db_table': 'user'},
        ),
        migrations.CreateModel(
            name='CinemaHall',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('screen_type', models.CharField(db_column='ekraani_tüüp', default='2D', max_length=20)),
                ('capacity', models.PositiveSmallIntegerField(db_column='mahutavus')),
                ('cinema', models.ForeignKey(db_column='kino_id', on_delete=django.db.models.deletion.PROTECT, related_name='halls', to='cinema.cinema')),
            ],
            options={'db_table': 'kinosaalid'},
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('row', models.CharField(db_column='rida', max_length=3)),
                ('number', models.PositiveSmallIntegerField(db_column='istekoht')),
                ('hall', models.ForeignKey(db_column='kinosaal_id', on_delete=django.db.models.deletion.CASCADE, related_name='seats', to='cinema.cinemahall')),
            ],
            options={'db_table': 'istekohad'},
        ),
        migrations.CreateModel(
            name='Screening',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('start_time', models.DateTimeField(db_column='algus_aeg')),
                ('end_time', models.DateTimeField(db_column='lopu_aeg')),
                ('language', models.CharField(blank=True, db_column='keel', max_length=50, null=True)),
                ('subtitles', models.CharField(blank=True, db_column='subtiitrid', max_length=50, null=True)),
                ('base_price', models.DecimalField(db_column='alghind', decimal_places=2, max_digits=8)),
                ('hall', models.ForeignKey(db_column='saali_id', on_delete=django.db.models.deletion.CASCADE, related_name='screenings', to='cinema.cinemahall')),
                ('movie', models.ForeignKey(db_column='filmi_id', on_delete=django.db.models.deletion.CASCADE, related_name='screenings', to='cinema.movie')),
            ],
            options={'db_table': 'seansid'},
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(db_column='staatus', default='ootel', max_length=20)),
                ('total', models.DecimalField(db_column='kogusumma', decimal_places=2, max_digits=8)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='loodud')),
                ('screening', models.ForeignKey(db_column='seansi_id', on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='cinema.screening')),
                ('user', models.ForeignKey(db_column='kasutaja_id', on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='cinema.user')),
            ],
            options={'db_table': 'broneeringud'},
        ),
        migrations.CreateModel(
            name='BookedSeat',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('price', models.DecimalField(db_column='hind', decimal_places=2, max_digits=8)),
                ('booking', models.ForeignKey(db_column='broneeringu_id', on_delete=django.db.models.deletion.CASCADE, related_name='booked_seats', to='cinema.booking')),
                ('screening', models.ForeignKey(db_column='seansi_id', on_delete=django.db.models.deletion.CASCADE, related_name='booked_seats', to='cinema.screening')),
                ('seat', models.ForeignKey(db_column='istekoha_id', on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='cinema.seat')),
            ],
            options={'db_table': 'broneeritud_kohad'},
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(db_column='summa', decimal_places=2, max_digits=8)),
                ('method', models.CharField(db_column='makseviis', max_length=30)),
                ('status', models.CharField(db_column='staatus', max_length=20)),
                ('reference', models.CharField(blank=True, db_column='makse_viide', max_length=255, null=True)),
                ('paid_at', models.DateTimeField(blank=True, db_column='makstud', null=True)),
                ('booking', models.ForeignKey(db_column='broneeringu_id', on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='cinema.booking')),
            ],
            options={'db_table': 'maksed'},
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('rating', models.PositiveSmallIntegerField(blank=True, db_column='hinnang', null=True, validators=[MinValueValidator(1), MaxValueValidator(5)])),
                ('comment', models.TextField(blank=True, db_column='kommentaar', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='loodud')),
                ('movie', models.ForeignKey(db_column='filmi_id', on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='cinema.movie')),
                ('user', models.ForeignKey(db_column='kasutaja_id', on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='cinema.user')),
            ],
            options={'db_table': 'arvustused'},
        ),
        migrations.CreateModel(
            name='MovieGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(db_column='žanri_id', on_delete=django.db.models.deletion.CASCADE, to='cinema.genre')),
                ('movie', models.ForeignKey(db_column='filmi_id', on_delete=django.db.models.deletion.CASCADE, to='cinema.movie')),
            ],
            options={'db_table': 'filmid_zanrid'},
        ),
        migrations.AddField(
            model_name='movie',
            name='genres',
            field=models.ManyToManyField(related_name='movies', through='cinema.MovieGenre', to='cinema.genre'),
        ),
        migrations.AddConstraint(
            model_name='seat',
            constraint=models.UniqueConstraint(fields=('hall', 'row', 'number'), name='unique_seat_in_hall'),
        ),
        migrations.AddConstraint(
            model_name='screening',
            constraint=models.CheckConstraint(condition=models.Q(('end_time__gt', models.F('start_time'))), name='screening_end_after_start'),
        ),
        migrations.AddConstraint(
            model_name='bookedseat',
            constraint=models.UniqueConstraint(fields=('screening', 'seat'), name='unique_booked_seat_per_screening'),
        ),
        migrations.AddConstraint(
            model_name='moviegenre',
            constraint=models.UniqueConstraint(fields=('movie', 'genre'), name='unique_movie_genre'),
        ),
    ]
