from django.db import models
from django.contrib.auth.models import User

class Forecast(models.Model):
    CATEGORY_CHOICES = [
        ('grain', 'Зерновые культуры'),
        ('veg', 'Овощи'),
        ('fruit', 'Плодовые культуры'),
        ('weather', 'Погодные риски'),
        ('market', 'Рыночные цены'),
    ]

    title = models.CharField('Название прогноза', max_length=200)
    category = models.CharField('Категория', max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField('Описание')
    region = models.CharField('Регион', max_length=120, default='Россия')
    price = models.DecimalField('Цена, ₽', max_digits=10, decimal_places=2, default=0)
    file = models.FileField('Файл прогноза', upload_to='forecasts/', blank=True, null=True)
    chart_html = models.TextField(
        'HTML-прогноз с графиками',
        blank=True,
        default='',
        help_text='HTML-разметка с графиками, отображается в кабинете'
    )
    created_at = models.DateTimeField('Дата загрузки', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Загрузил')

    class Meta:
        verbose_name = 'Прогноз'
        verbose_name_plural = 'Прогнозы'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases', verbose_name='Пользователь')
    forecast = models.ForeignKey(Forecast, on_delete=models.CASCADE, verbose_name='Прогноз')
    purchased_at = models.DateTimeField('Дата приобретения', auto_now_add=True)

    class Meta:
        verbose_name = 'Приобретённая услуга'
        verbose_name_plural = 'Приобретённые услуги'
        unique_together = ('user', 'forecast')
        ordering = ['-purchased_at']

    def __str__(self):
        return f'{self.user.username} → {self.forecast.title}'