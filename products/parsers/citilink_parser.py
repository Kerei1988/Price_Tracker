import requests
from bs4 import BeautifulSoup as bs


class CitilinkParser:
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'Referer': 'https://www.citilink.ru/',
    }

    home_url = "https://www.citilink.ru/"


    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(CitilinkParser.headers)


    def price_parser(self, url):
        res = self.session.get(url)
        soup = bs(res.text, 'lxml')
        outer_span = soup.select_one('[data-meta-is-total="notTotal"]')
        price = self.clean_price(outer_span.text)
        return price
    
    def clean_price(self, line):
        line = line.strip().replace('₽', '').replace(' ', '')
        return int(line) 



# if __name__ == '__main__':
#     product_url = 'https://www.citilink.ru/product/smartfon-apple-iphone-17-pro-max-a3526-1tb-temno-sinii-3g-4g-2sim-6-9-2134318/'
#     pars = CitilinkParser()
#     print(pars.price_parser(product_url))