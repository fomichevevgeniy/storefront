from django.db import models
from django.core.validators import MinValueValidator
from uuid import uuid4
from django.conf import settings
from django.contrib import admin

# Create your models here.

class Promotion(models.Model):
    description = models.CharField(max_length=255, verbose_name='Описание')
    discount = models.FloatField(verbose_name='Процент скидки')

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'


class Collection(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    feature_product = models.ForeignKey('Product', on_delete=models.SET_NULL,
                                        blank=True, null=True,
                                        related_name='+',
                                        verbose_name='Рекомендуемый товар')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название товара')
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    unit_price = models.DecimalField(max_digits=6, decimal_places=2,
                                     validators=[MinValueValidator(1)],
                                     verbose_name='Цена за шт')
    last_update = models.DateTimeField(auto_now_add=True, verbose_name='Время обновления')
    inventory = models.IntegerField(verbose_name='Кол-во на складе', default=0)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT,
                                   verbose_name='Категория', related_name='products')
    promotion = models.ManyToManyField(Promotion, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold')
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                default=None)
    phone = models.CharField(max_length=255, blank=True, null=True,
                             verbose_name='Номер телефона')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES,
                                  default=MEMBERSHIP_BRONZE, verbose_name='Статус')

    def __str__(self):
        return f'{self.user.first_name} - {self.user.last_name}'

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Cart(models.Model):
    # У корзины будет сложный id который сложнее подобрать и хранить его будет frontend
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина',
                             related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                verbose_name='Товар')
    quantity = models.PositiveIntegerField(verbose_name='Кол-во товаров')

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзинах'


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]
    placed_at = models.DateTimeField(auto_now_add=True, verbose_name='Время оформления')
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES,
                                      default=PAYMENT_STATUS_PENDING,
                                      verbose_name='Статус оплаты')
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, verbose_name='Заказ',
                              related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Товар')
    quantity = models.PositiveIntegerField(verbose_name='Кол-во товаров')
    unit_price = models.DecimalField(max_digits=6, decimal_places=2,
                                     verbose_name='Цена за шт')

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказах'


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(verbose_name='Описание')
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

class Address(models.Model):
    street = models.CharField(max_length=255, verbose_name='Улица')
    city = models.CharField(max_length=255, verbose_name='Город')
    house = models.CharField(max_length=255, verbose_name='Дом')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,
                                 verbose_name='Покупатель')
    type = models.BooleanField(default=False, verbose_name='Тип')
    # 0 - Адрес клиента  1 - адрес пункта выдачи

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='images')
    image = models.ImageField(upload_to='store/images')















