from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Sum



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11)
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
    requestion = models.ForeignKey(
        'Requestion',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Заявка на аренду',
        related_name='boxes'
    )

    def __str__(self):
        return self.box_number


class Requestion(models.Model):
    """Запрос на хранение вещей."""

    class Status(models.TextChoices):
        """Статусы заявко
            SEND - заявка отправлена
            VIEWED - заявка просмотрена оператором
            CONTACTED - с клиентом связались для уточнения деталей и оплаты
            PAID - оплачено
            DELIVERED - доставляется
            FINISHED - заявка завершена(либо клиент
            отказался либо товар приехал).
        """
        SEND = 'SD', 'Send'
        VIEWED = 'VD', 'Viewed'
        CONTACTED = 'CD', 'Contacted'
        PAID = 'PD', 'Paid'
        DELIVERED = 'DD', 'Delivered'
        FINISHED = 'FD', 'Finished'

    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        verbose_name="Арендатор",
        related_name="rents",
        null=True,
        blank=True,
    )
    mail = models.EmailField(
        blank=True,
        verbose_name='Почта пользователя',
    )
    """
    box = models.ForeignKey(
        Box,
        on_delete=models.CASCADE,
        verbose_name="Бокс",
        related_name="rents",
        null=True,
        blank=True,
    )
    """
    created_at = models.DateField(
        verbose_name="Дата создания",
        default=timezone.now,
        db_index=True,
    )
    expiration_at = models.DateField(
        verbose_name="Дата окончания аренды",
        blank=True,
        null=True,
        db_index=True,
    )
    price = models.PositiveSmallIntegerField(
        null=True,
        verbose_name='стоимость хранения за год',
        help_text='высчитывается после обработки заявки',
    )
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.SEND,
        verbose_name='статус заявки',
    )

    class Meta:
        verbose_name = "Аренда"
        verbose_name_plural = "Аренды"



@receiver(post_save, sender=Box) 
def correct_price(sender, instance, created, **kwargs):
    if instance.requestion:
        req = instance.requestion
        new_price = Requestion.objects.filter(id=req.id)\
                                      .aggregate(Sum('boxes__price'))
        req.price = new_price['boxes__price__sum']
        req.save(update_fields=['price'])


@receiver(post_save, sender=Requestion) 
def correct_price(sender, instance, created, **kwargs):
    if instance.boxes.exists():
        req_price = instance.boxes.all().aggregate(Sum('price'))
        instance.price = req_price['price__sum']

