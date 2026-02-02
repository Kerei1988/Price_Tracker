from django.core.management.base import BaseCommand
from products.services import get_parser_service
from products.models import Product


class Command(BaseCommand):
	help = 'Парсит цены для всех товаров'

	def handle(self, *args, **options):
		parse_service = get_parser_service()
		products = Product.objects.filter(store__is_active=True)

		success = 0
		failed = 0

		for product in products:
			try:
				if parse_service.parser_product(product):
					success += 1
				
				else:
					failed += 1

			except Exception as e:
				self.stdout.write(f"Ошибка с товаром {product.id} - {e}")
				failed += 1

		self.stdout.write(f"Итоги:")
		self.stdout.write(f'Успешно: {success}')
		self.stdout.write(f'С ошибками: {failed}') 