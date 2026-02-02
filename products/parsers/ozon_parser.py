# products/parsers/ozon_parser.py
import requests
from bs4 import BeautifulSoup
from decimal import Decimal
import re

class OzonParser:
    """Парсер для Ozon с твоим рабочим селектором"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Referer': 'https://www.ozon.ru/',
        }
    
    def clean_price(self, price_text):
        """Очистка цены Ozon"""
        if not price_text:
            return None
        
        # Убираем неразрывные пробелы ( ) и другие символы
        # В твоей цене: "165 218 ₽" - есть неразрывные пробелы \u2009
        cleaned = re.sub(r'[^\d.,]', '', str(price_text))
        cleaned = cleaned.replace(',', '.')
        
        try:
            return Decimal(cleaned)
        except:
            return None
    
    def parse_price(self, url):
        """
        Парсинг цены с Ozon
        
        Args:
            url (str): Ссылка на товар Ozon
            
        Returns:
            Decimal or None: Цена или None если ошибка
        """
        try:
            print(f"🔍 Парсим Ozon: {url}")
            
            # 1. Загружаем страницу
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # 2. Проверяем блокировку
            if 'доступ ограничен' in response.text.lower():
                print("❌ Доступ ограничен (возможно капча)")
                return None
            
            # 3. Парсим HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 4. Ищем цену по ТВОЕМУ СЕЛЕКТОРУ
            price = None
            
            # Основной селектор (который у тебя работает)
            price_element = soup.find('span', class_='tsHeadline600Large')
            
            if price_element:
                price_text = price_element.get_text(strip=True)
                price = self.clean_price(price_text)
                
                if price:
                    print(f"✅ Нашли через tsHeadline600Large: {price_text} → {price}₽")
                    return price
                else:
                    print(f"❌ Не удалось очистить цену из: {price_text}")
            else:
                print("❌ Не нашли элемент с классом tsHeadline600Large")
                
                # Альтернативные селекторы на всякий случай
                alternative_selectors = [
                    ('span[class*="price"]', 'span с price в классе'),
                    ('div[class*="price"]', 'div с price в классе'),
                    ('[data-widget="webPrice"]', 'data-widget webPrice'),
                    ('[data-test-id="price"]', 'data-test-id price'),
                ]
                
                for selector, description in alternative_selectors:
                    try:
                        element = soup.select_one(selector)
                        if element:
                            alt_text = element.get_text(strip=True)
                            alt_price = self.clean_price(alt_text)
                            if alt_price:
                                print(f"⚠️ Нашли через {description}: {alt_price}₽")
                                return alt_price
                    except:
                        continue
            
            # 5. Если совсем ничего не нашли
            print("❌ Цена не найдена. Возможные причины:")
            print("   - Изменилась структура сайта")
            print("   - Товара нет в наличии")
            print("   - Нужна авторизация")
            
            # Для отладки сохраним HTML
            with open('ozon_last_error.html', 'w', encoding='utf-8') as f:
                f.write(response.text[:5000])  # Первые 5000 символов
            print("   Сохранён HTML для отладки: ozon_last_error.html")
            
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка сети: {e}")
            return None
        except Exception as e:
            print(f"❌ Неожиданная ошибка: {e}")
            return None
    
    def test(self, url=None):
        """Тест парсера"""
        if not url:
            # Твой тестовый URL с iPhone
            url = "https://www.ozon.ru/product/smartfon-apple-iphone-15-128gb-chernyy-1259611403/"
        
        print("🧪 Тестируем парсер Ozon")
        print("=" * 50)
        
        price = self.parse_price(url)
        
        if price:
            print(f"\n🎉 УСПЕХ! Цена: {price}₽")
            return True
        else:
            print("\n❌ Не удалось получить цену")
            return False

# Простой тест
if __name__ == "__main__":
    parser = OzonParser()
    
    # Тест с твоим URL
    test_url = "https://www.ozon.ru/product/smartfon-apple-iphone-15-128gb-chernyy-1259611403/"
    url_test = 'https://www.ozon.ru/product/apple-smartfon-iphone-16-esim-sim-8-512-gb-belyy-1687844432/?at=16tLGqYM4iKEZmXQILWQlWNCLL68XMfgBggE4cmpzmwo'
    
    success = parser.test(test_url)
    
    if success:
        print("\n✅ Парсер Ozon работает!")
    else:
        print("\n❌ Нужно отладить селекторы")