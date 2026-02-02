from django.db import models
from django.contrib.auth.models import User


class Store(models.Model):

	name = models.CharField(max_length=100, verbose_name='Название магазина')
	base_url = models.URLField(verbose_name='Базовый URL магазин')
	is_active = models.BooleanField(default=True, verbose_name='Активен')
	
	
	def __str__(self):
		return self.name
	
	class Meta:

		verbose_name = 'Магазин'
		verbose_name_plural = 'Магазины'
		ordering = ['name']


class Product(models.Model):

	name = models.CharField(max_length=200, verbose_name='Название товара')
	url = models.URLField(verbose_name='ссылка на товар')
	store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name='Магазин')
	target_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Целевая цена (₽)')
	current_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Текущая цена (₽)')
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
	update_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

	def __str__(self):
		price = f"{self.current_price}₽" if self.current_price else 'Нет цены'
		return f"{self.name} - {price}"
	
	class Meta:
		verbose_name = 'Товар'
		verbose_name_plural = "Товары"
		ordering = ['-update_at', 'name']


class PriceHistory(models.Model):

	product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Название товара')
	price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена (₽)')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

	def __str__(self):
		return f'Продукт: {self.product}, цена: {self.price}, получена: {self.created_at} '
	
	class Meta:
		verbose_name = 'История цены'
		verbose_name_plural = 'История цен'
		ordering = ['-created_at']

