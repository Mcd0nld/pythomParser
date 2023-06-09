#pip install beautifulsoup4 requests lxml
import random
from time import sleep

import requests
from bs4 import BeautifulSoup
import json
import csv

# ссылка на нашу страницу
# url = "https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie"
#
headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
#
# req = requests.get(url)
# src = req.text
# # print(src)

#сохраняем нашу страницу в файл
# with open("index.html", "w", encoding="utf-8-sig") as file:
#     file.write(src)

# открываем, читаем наш файл и сохраняем код страницы в переменную src
# with open("index.html", encoding="utf-8-sig") as file:
#     src = file.read()
#
# soup = BeautifulSoup(src, "lxml")
#
# all_products = soup.find_all(class_="mzr-tc-group-item-href")
#
# for item in all_products:
#     item_text = item.text
#     item_href = "https://health-diet.ru" + item.get("href")
#     print(f"{item_text}: {item_href}")

# сохраняем данные в словарь
# all_products_dict = {}
# for item in all_products:
#     item_text = item.text
#     item_href = "https://health-diet.ru" + item.get("href")
#
#     all_products_dict[item_text] = item_href

# сохранение данных словая в json файл, сохраняет время на поиск инф в интернете
# with open("all_products_dict.json", "w", encoding="utf-8-sig") as file:
#     json.dump(all_products_dict, file, indent=4, ensure_ascii=False)

with open("all_products_dict.json", encoding="utf-8-sig") as file:
    all_categories = json.load(file)

iteration_count = int(len(all_categories)) - 1
count = 0
print(f"Всего итераций: {iteration_count}")

for category_name, category_href in all_categories.items():


    # заменяем не нужные символы на нижний слэш
    rep = [",", " ", "-", "'"]
    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, "_")

    req = requests.get(url=category_href, headers=headers)
    src = req.text

    with open(f"data/{count}_{category_name}.html", "w", encoding="utf-8-sig")as file:
        file.write(src)

    with open(f"data/{count}_{category_name}.html", encoding="utf-8-sig")as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    # проверяем саму страницу на наличие таблицы с продуктами
    alert_block = soup.find(class_="uk-alert-danger")
    if alert_block is not None:
        continue

    # собираем заголовки таблицы
    table_head = soup.find(class_="mzr-tc-group-table").find("tr").find_all("th")
    product = table_head[0].text
    calories = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    carbohydrates = table_head[4].text

    with open(f"data/{count}_{category_name}.csv", "w", encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(
            (
                product,
                calories,
                proteins,
                fats,
                carbohydrates
            )
        )

    # собираем данные продуктов
    products_data = soup.find(class_="mzr-tc-group-table").find("tbody").find_all("tr")

    products_info = []
    for item in products_data:
        product_tds = item.find_all("td")

        title = product_tds[0].find("a").text
        calories = product_tds[1].text
        proteins = product_tds[2].text
        fats = product_tds[3].text
        carbohydrates = product_tds[4].text

        products_info.append(
            {
                "Title": title,
                "Calories": calories,
                "Proteins": proteins,
                "Fats": fats,
                "Carbohydrates": carbohydrates
            }
        )

        with open(f"data/{count}_{category_name}.csv", "a", encoding="utf-8-sig") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(
                (
                    title,
                    calories,
                    proteins,
                    fats,
                    carbohydrates
                )
            )
    with open(f"data/{count}_{category_name}.json", "a", encoding="utf-8-sig") as file:
        json.dump(products_info, file, indent=4, ensure_ascii=False)

    count +=1
    print(f"# Итерация {count}. {category_name} записан...")
    iteration_count = iteration_count - 1

    if iteration_count == 0:
        print("Работа завершена")
        break

    print(f"Осталось итераций: {iteration_count}")
    sleep(random.randrange(2, 4))