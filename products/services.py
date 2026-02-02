from .models import Product, PriceHistory


class ParserService:

    def __init__(self):
        self.parsers = {}


    def add_parsers(self, name_store, parser):
        self.parsers[name_store] = parser

    def parser_product(self, product):
        print(f'Начинаем парсить {product.name}')
        parser = self.parsers[product.store.name]
    

        if not parser:
            print(f'Нет парсера для магазина {product.store.name}')
            return False

        price = parser.price_parser(product.url)


        if price:
            PriceHistory.objects.create(
                product=product,
                price=price
            )
        
            product.current_price = price
            product.save()
            print(product)
            return True
        else:
            print(f"Не удалось получить цену")
            return False


from .parsers.citilink_parser import CitilinkParser


def get_parser_service():
    service = ParserService()
    service.add_parsers('Citilink', CitilinkParser())
    return service
    
