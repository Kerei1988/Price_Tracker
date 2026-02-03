from django.core.management.base import BaseCommand
from products.services import get_parser_service
from products.models import Product


class Command(BaseCommand):
    help = 'Парсит цены для всех товаров или конкретного товара'

    # ДОБАВЬ ЭТУ ФУНКЦИЮ для добавления аргументов
    def add_arguments(self, parser):
        parser.add_argument(
            '--product',
            type=int,
            help='ID конкретного товара для парсинга',
        )
        parser.add_argument(
            '--store',
            type=int,
            help='ID магазина для парсинга всех его товаров',
        )

    # ИЗМЕНИ ЭТУ ФУНКЦИЮ для обработки аргументов
    def handle(self, *args, **options):
        parse_service = get_parser_service()
        
        # ПОЛУЧАЕМ АРГУМЕНТЫ ИЗ КОМАНДНОЙ СТРОКИ
        product_id = options.get('product')
        store_id = options.get('store')
        
        # ФИЛЬТРУЕМ ТОВАРЫ В ЗАВИСИМОСТИ ОТ АРГУМЕНТОВ
        products = Product.objects.filter(store__is_active=True)
        
        if product_id:
            # Если указан конкретный товар
            products = products.filter(id=product_id)
            self.stdout.write(f"Парсим товар с ID: {product_id}")
        
        elif store_id:
            # Если указан магазин
            products = products.filter(store_id=store_id)
            self.stdout.write(f"Парсим все товары магазина ID: {store_id}")
        
        else:
            # Если аргументов нет - парсим все товары
            self.stdout.write("Парсим все товары")
        
        success = 0
        failed = 0

        for product in products:
            try:
                if parse_service.parser_product(product):
                    self.stdout.write(f"✓ Товар {product.id}: {product.name}")
                    success += 1
                else:
                    self.stdout.write(f"✗ Товар {product.id}: не удалось спарсить")
                    failed += 1

            except Exception as e:
                self.stdout.write(f"✗ Ошибка с товаром {product.id} - {e}")
                failed += 1

        self.stdout.write(f"\nИтоги:")
        self.stdout.write(f'Успешно: {success}')
        self.stdout.write(f'С ошибками: {failed}')