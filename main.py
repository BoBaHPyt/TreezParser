import asyncio
import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from TreezParser import TreezParser


def export_to_google_sheets(df, crenditals, sheet_id, worksheet_id):
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    crenditals = ServiceAccountCredentials.from_json_keyfile_name(crenditals, scope)
    client = gspread.authorize(crenditals)
    
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.get_worksheet(worksheet_id)
    sheet.values_clear(f"{worksheet.title}!A2:E10000")
    worksheet.update(df)


async def main():
    products = [["Категория", "Наименование", "Артикул", "Цена", "Остаток", "Обновлено"]]
    async with TreezParser() as tp:
        await tp.login("zakupki@best-coll.ru", "Collection1")
        products += await tp.get_all_products()
    products[1].append(datetime.datetime.now().strftime("%d.%m.%Y %H:%M"))
    export_to_google_sheets([] + products, "gapi.json", "1sgVk3nJTAc6ihG16SFWiRlCWUTFTF6bhHu1c8G8yDhk", 0)

asyncio.run(main())
