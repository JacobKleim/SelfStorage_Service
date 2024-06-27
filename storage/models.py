from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=1)
    full_name = models.CharField(max_length=255)

    def str(self):
        return self.user.username


class Storehouse(models.Model):
    city = models.CharField(
        verbose_name='Город',
        max_length=50,
        db_index=True)
    address = models.CharField(
        verbose_name="Адрес склада",
        max_length=200,
        db_index=True
    )
    description = models.TextField(
        verbose_name="Описание"
    )
    road = models.TextField(
        verbose_name="описание проезда"
    )
    contact_phone = PhoneNumberField(
        verbose_name="Контактный телефон"
    )
    temperature = models.SmallIntegerField(
        verbose_name="Температура на складе",
        db_index=True,
        validators=[MinValueValidator(-60), MaxValueValidator(60)]
    )

    def __str__(self):
        return f"{self.city}, {self.address}"


class Box(models.Model):
    storehouse = models.ForeignKey(
        Storehouse,
        on_delete=models.CASCADE,
        verbose_name='Склад',
        related_name='boxes'
    )
    box_number = models.CharField(
        'номер бокса',
        max_length=20,
        db_index=True,
        unique=True
    )
    floor = models.CharField(
        verbose_name="Этаж",
        max_length=3
    )
    length = models.FloatField(
        verbose_name='длина',
        validators=[MinValueValidator(0)]
    )
    width = models.FloatField(
        verbose_name='ширина',
        validators=[MinValueValidator(0)]
    )
    height = models.FloatField(
        verbose_name='высота',
        validators=[MinValueValidator(0)]
    )
    price = models.DecimalField(
        verbose_name='цена',
        max_digits=10,
        decimal_places=2,
        db_index=True,
        validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return self.box_number


class StorehouseImage(models.Model):
    number_pic = models.PositiveIntegerField(
        verbose_name='Номер картинки',
        default=0,
        db_index=True,
        blank=True
    )
    storehouse = models.ForeignKey(
        Storehouse,
        verbose_name='Склад',
        on_delete=models.CASCADE,
        related_name='images')
    img = models.ImageField(
        verbose_name='Картинка'
    )

    class Meta:
        ordering = ['number_pic']

    def __str__(self):
        return f'{self.number_pic} {self.storehouse}'
