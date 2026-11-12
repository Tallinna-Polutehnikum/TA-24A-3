from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0003_screening_screening_start_id_idx'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='user',
            table='kasutajad',
        ),
        migrations.AlterField(
            model_name='seat',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='movie',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='movie',
            name='poster_url',
            field=models.URLField(blank=True, db_column='plakati_url', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='trailer_url',
            field=models.URLField(blank=True, db_column='treileri_url', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='is_featured',
            field=models.BooleanField(db_column='esiletõstetud', default=False),
        ),
        migrations.AlterField(
            model_name='genre',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='screening',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='booking',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='bookedseat',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='payment',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='review',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
