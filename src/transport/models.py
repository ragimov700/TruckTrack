from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models

from transport.constants import (
    MAX_CAPACITY,
    MAX_CARGO_WEIGHT,
    MIN_CAPACITY,
    MIN_CARGO_WEIGHT,
    NUMBER_REGEX,
)


class Location(models.Model):
    """
    Модель локации. Содержит информацию о городе, штате и почтовом индексе,
    а также широте и долготе.
    """
    city = models.CharField(max_length=100, verbose_name='город')
    state = models.CharField(max_length=2, verbose_name='штат')
    zip_code = models.CharField(max_length=5, verbose_name='почтовый индекс')
    latitude = models.DecimalField(
        max_digits=8,
        decimal_places=5,
        verbose_name='широта'
    )
    longitude = models.DecimalField(
        max_digits=8,
        decimal_places=5,
        verbose_name='долгота'
    )

    def __str__(self):
        return f'{self.city}, {self.state} {self.zip_code}'

    class Meta:
        verbose_name = 'локация'
        verbose_name_plural = 'локации'


class Cargo(models.Model):
    """
    Модель груза. Содержит информацию о местах погрузки и разгрузки,
    весе и описании груза.
    """
    pickup_location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='pickups',
        verbose_name='место погрузки'
    )
    delivery_location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='deliveries',
        verbose_name='место разгрузки'
    )
    weight = models.PositiveIntegerField(
        validators=(
            MinValueValidator(MIN_CARGO_WEIGHT),
            MaxValueValidator(MAX_CARGO_WEIGHT)
        ),
        verbose_name='вес'
    )
    description = models.TextField(
        max_length=1000,
        verbose_name='описание груза'
    )

    def __str__(self):
        return f'Груз из {self.pickup_location} в {self.delivery_location}'

    class Meta:
        verbose_name = 'груз'
        verbose_name_plural = 'грузы'


class Truck(models.Model):
    """
    Модель грузовика. Содержит информацию о номерном знаке, грузоподъемности
    и текущем местоположении.
    """
    plate_number = models.CharField(
        max_length=6,
        verbose_name='номерной знак',
        unique=True,
        validators=(
            RegexValidator(
                regex=NUMBER_REGEX,
                message='Номерной знак должен иметь формат: "1234A"'
            ),
        )
    )
    capacity = models.PositiveIntegerField(
        verbose_name='грузоподъемность',
        validators=(
            MinValueValidator(MIN_CAPACITY),
            MaxValueValidator(MAX_CAPACITY)
        )
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='местоположение'
    )

    def __str__(self):
        return f'Грузовик {self.plate_number}'

    class Meta:
        verbose_name = 'грузовик'
        verbose_name_plural = 'грузовики'
