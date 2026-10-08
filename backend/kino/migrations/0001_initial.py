from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Cinema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='kino_nimi', max_length=255)),
                ('street_address', models.CharField(db_column='tänava_aadress', max_length=255)),
                ('city', models.CharField(db_column='linn', max_length=255)),
                ('postal_code', models.CharField(db_column='postiindeks', max_length=32)),
                ('country', models.CharField(db_column='riik', max_length=255)),
            ],
            options={
                'db_table': 'kino',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='nimi', max_length=50)),
            ],
            options={
                'db_table': 'žanrid',
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_column='pealkiri', max_length=255)),
                ('description', models.TextField(blank=True, db_column='kirjeldus', null=True)),
                ('duration_minutes', models.PositiveSmallIntegerField(db_column='filmi_pikkus', default=0)),
                ('release_date', models.DateField(blank=True, db_column='väljalaskekuupäev', null=True)),
                ('age_rating', models.CharField(blank=True, db_column='vanusepiirang', max_length=10, null=True)),
                ('language', models.CharField(blank=True, db_column='keel', max_length=50, null=True)),
                ('poster_url', models.CharField(blank=True, db_column='plakati_url', max_length=500, null=True)),
                ('trailer_url', models.CharField(blank=True, db_column='treileri_url', max_length=500, null=True)),
                ('is_small_value', models.BooleanField(db_column='väikeväärtus', default=False)),
            ],
            options={
                'db_table': 'filmid',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(db_column='user', max_length=255, unique=True)),
                ('first_name', models.CharField(max_length=1024)),
                ('last_name', models.CharField(max_length=1024)),
                ('phone_number', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=1024, unique=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('password_hash', models.TextField()),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='Auditorium',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('screen_type', models.CharField(db_column='ekraani_tüüp', default='2D', max_length=20)),
                ('capacity', models.PositiveSmallIntegerField(db_column='mahutavus')),
                ('cinema', models.ForeignKey(db_column='kino_id', on_delete=django.db.models.deletion.PROTECT, to='kino.cinema')),
            ],
            options={
                'db_table': 'kinosaalid',
            },
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row', models.CharField(db_column='rida', max_length=3)),
                ('number', models.PositiveSmallIntegerField(db_column='istekoht')),
                ('auditorium', models.ForeignKey(db_column='saali_id', on_delete=django.db.models.deletion.CASCADE, to='kino.auditorium')),
            ],
            options={
                'db_table': 'istekohad',
            },
        ),
        migrations.CreateModel(
            name='Screening',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starts_at', models.DateTimeField(db_column='algus_aeg')),
                ('ends_at', models.DateTimeField(db_column='lopu_aeg')),
                ('language', models.CharField(blank=True, db_column='keel', max_length=50, null=True)),
                ('subtitles', models.CharField(blank=True, db_column='subtiitrid', max_length=50, null=True)),
                ('price', models.DecimalField(db_column='alghind', decimal_places=2, max_digits=8)),
                ('auditorium', models.ForeignKey(db_column='saali_id', on_delete=django.db.models.deletion.PROTECT, to='kino.auditorium')),
                ('movie', models.ForeignKey(db_column='filmi_id', on_delete=django.db.models.deletion.PROTECT, to='kino.movie')),
            ],
            options={
                'db_table': 'seansid',
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(db_column='staatus', default='ootel', max_length=20)),
                ('total', models.DecimalField(db_column='kogusumma', decimal_places=2, max_digits=8)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='loodud')),
                ('screening', models.ForeignKey(db_column='seansi_id', on_delete=django.db.models.deletion.PROTECT, to='kino.screening')),
                ('user', models.ForeignKey(db_column='kasutaja_id', on_delete=django.db.models.deletion.PROTECT, to='kino.user')),
            ],
            options={
                'db_table': 'broneeringud',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(db_column='summa', decimal_places=2, max_digits=8)),
                ('method', models.CharField(db_column='makseviis', max_length=30)),
                ('status', models.CharField(db_column='staatus', max_length=20)),
                ('reference', models.CharField(blank=True, db_column='makse_viide', max_length=255, null=True)),
                ('paid_at', models.DateTimeField(blank=True, db_column='makstud', null=True)),
                ('booking', models.ForeignKey(db_column='broneeringu_id', on_delete=django.db.models.deletion.CASCADE, to='kino.booking')),
            ],
            options={
                'db_table': 'maksed',
            },
        ),
        migrations.CreateModel(
            name='ReservedSeat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(db_column='hind', decimal_places=2, max_digits=8)),
                ('booking', models.ForeignKey(db_column='broneeringu_id', on_delete=django.db.models.deletion.CASCADE, to='kino.booking')),
                ('screening', models.ForeignKey(db_column='seansi_id', on_delete=django.db.models.deletion.PROTECT, to='kino.screening')),
                ('seat', models.ForeignKey(db_column='istekoha_id', on_delete=django.db.models.deletion.PROTECT, to='kino.seat')),
            ],
            options={
                'db_table': 'broneeritud_kohad',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(blank=True, db_column='hinnang', null=True)),
                ('comment', models.TextField(blank=True, db_column='kommentaar', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='loodud')),
                ('movie', models.ForeignKey(db_column='filmi_id', on_delete=django.db.models.deletion.PROTECT, to='kino.movie')),
                ('user', models.ForeignKey(db_column='kasutaja_id', on_delete=django.db.models.deletion.PROTECT, to='kino.user')),
            ],
            options={
                'db_table': 'arvustused',
            },
        ),
        migrations.AddConstraint(
            model_name='seat',
            constraint=models.UniqueConstraint(fields=('auditorium', 'row', 'number'), name='istekoht_saali_rea_num_uniq'),
        ),
        migrations.AddConstraint(
            model_name='screening',
            constraint=models.CheckConstraint(condition=models.Q(('ends_at__gt', models.F('starts_at'))), name='seans_lopp_parast_algust'),
        ),
        migrations.AddConstraint(
            model_name='reservedseat',
            constraint=models.UniqueConstraint(fields=('screening', 'seat'), name='broneeritud_seans_iste_uniq'),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.CheckConstraint(
                condition=models.Q(rating__isnull=True) | (
                    models.Q(rating__gte=1) & models.Q(rating__lte=5)
                ),
                name='arvustus_hinnang_1_5',
            ),
        ),
    ]
