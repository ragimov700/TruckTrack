# Generated by Django 4.2.11 on 2024-03-24 07:32

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(1000)], verbose_name='вес')),
                ('description', models.TextField(max_length=1000, verbose_name='описание груза')),
            ],
            options={
                'verbose_name': 'груз',
                'verbose_name_plural': 'грузы',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100, verbose_name='город')),
                ('state', models.CharField(max_length=2, verbose_name='штат')),
                ('zip_code', models.CharField(max_length=5, validators=[django.core.validators.RegexValidator(message='Индекс должен иметь формат: "12345"', regex='^\\d{5}$')], verbose_name='почтовый индекс')),
                ('latitude', models.DecimalField(decimal_places=5, max_digits=8, verbose_name='широта')),
                ('longitude', models.DecimalField(decimal_places=5, max_digits=8, verbose_name='долгота')),
            ],
            options={
                'verbose_name': 'локация',
                'verbose_name_plural': 'локации',
            },
        ),
        migrations.CreateModel(
            name='Truck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plate_number', models.CharField(max_length=5, unique=True, validators=[django.core.validators.RegexValidator(message='Номерной знак должен иметь формат: "1234A"', regex='^[1-9]\\d{3}[A-Z]$')], verbose_name='номерной знак')),
                ('capacity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(1000)], verbose_name='грузоподъемность')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='transport.location', verbose_name='местоположение')),
            ],
            options={
                'verbose_name': 'грузовик',
                'verbose_name_plural': 'грузовики',
            },
        ),
        migrations.AddConstraint(
            model_name='location',
            constraint=models.UniqueConstraint(fields=('latitude', 'longitude'), name='unique_location'),
        ),
        migrations.AddField(
            model_name='cargo',
            name='delivery_location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deliveries', to='transport.location', verbose_name='место разгрузки'),
        ),
        migrations.AddField(
            model_name='cargo',
            name='pickup_location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pickups', to='transport.location', verbose_name='место погрузки'),
        ),
    ]
