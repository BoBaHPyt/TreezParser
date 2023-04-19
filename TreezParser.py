import asyncio

import aiohttp
import lxml.html
import tqdm


class TreezParser:
    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.session.headers.add("User-Agent", "Mozilla/5.0 (Windows NT 10.0; rv:112.0) Gecko/20100101 Firefox/112.0")
        self.products = []
        self._product_urls = self._product_urls_generator()

    async def __aenter__(self, *args, **kwargs):
        return self

    async def __aexit__(self, *args, **kwargs):
        await self.session.close()

    async def login(self, login, password):
        url = "https://treez.ru/local/templates/treez/include/auth_form.php"
        auth_data = {"backurl": "/",
                     "AUTH_FORM": "Y",
                     "TYPE": "AUTH",
                     "USER_LOGIN": login,
                     "USER_PASSWORD": password,
                     "Login": "Войти",
                     "ajax": "Y"}
        async with self.session.post(url, data=auth_data) as response:
            content = await response.text()
            assert "Авторизация прошла успешно" in content, f"Ошибка авторизации ({response.status} {content})"

    async def _product_urls_generator(self):
        async with self.session.get("https://treez.ru/sitemap.xml") as response:
            content = await response.read()
            document = lxml.html.fromstring(content)
            for url in tqdm.tqdm(document.xpath("//url/loc[contains(text(), \"/good/\")]/text()")):
                yield url

    async def product_parse_thread(self):
        while True:
            try:
                url = await self._product_urls.__anext__()
                async with self.session.get(url) as response:
                    content = await response.read()
                    document = lxml.html.fromstring(content)
                    name = document.xpath("//h1[@class=\"b-catalog-item__title\"]/text()")[0]
                    category = document.xpath("//div[@class=\"b-breadcrumbs\"]//a[@itemprop=\"item\"]/span/text()")[2]
                    mods = document.xpath("//form[@id=\"cart_options\"]/div[contains(@class, \"b-catalog-item__option\")]")
                    for mod in mods:
                        art = mod.xpath("./div/div[@class=\"b-catalog-item__option-code\"]/b/text()")[0]
                        price = mod.xpath("./div/div/@data-price")[0]
                        type = mod.xpath("./div/div/div/b[contains(text(), \"кашпо\")]/text()")
                        count = len(mod.xpath("./div/div/div/b/span[@data-svg=\"tree\"]")) * (10 if type else 50)
                        self.products.append([category, name, art, price, count])
            except:
                break

    async def get_all_products(self):
        await asyncio.gather(*[self.product_parse_thread() for i in range(20)])
        self.products.sort()
        return self.products
 