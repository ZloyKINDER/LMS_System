from django.contrib.auth.models import AbstractUser
from django.db import models
from materials.models import Course, Lesson
from .managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=35, verbose_name='Телефон', blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name='Город', blank=True, null=True)
    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='Аватар', blank=True, null=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  

    # Привязываем кастомный менеджер
    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Payment(models.Model):
    class PaymentMethod(models.TextChoices):
        CASH = 'cash', 'Наличные'
        TRANSFER = 'transfer', 'Перевод на счет'
        STRIPE = 'stripe', 'Stripe'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments', verbose_name='Пользователь')
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    paid_course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name='Оплаченный курс')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name='Оплаченный урок')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')
    payment_method = models.CharField(max_length=10, choices=PaymentMethod.choices, verbose_name='Способ оплаты')

    # Поля для Stripe
    stripe_product_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='ID продукта в Stripe')
    stripe_price_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='ID цены в Stripe')
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='ID сессии оплаты')
    payment_status = models.CharField(max_length=50, default='pending', verbose_name='Статус оплаты')
    payment_url = models.URLField(max_length=2000, blank=True, null=True, verbose_name='Ссылка на оплату')

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['-payment_date']

    def __str__(self):
        return f"{self.user.email} - {self.amount} руб. ({self.payment_date})"


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions', verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subscriptions', verbose_name='Курс')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата подписки')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ['user', 'course']  # Чтобы пользователь не мог подписаться на один курс дважды

    def __str__(self):
        return f"{self.user.email} подписан на {self.course.title}"