import requests
from bs4 import BeautifulSoup
import csv

for i in range(1, 34):
    url = f'https://mojim.com/twzlhc_{str(i).zfill(2)}.htm'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    songs = soup.select('.s_listA li a')

    data = []
    for song in songs:
        name = song['title']
        link = song['href']
        data.append([name, link])

    # 檢查重複資料
    existing_data = []
    with open('artists.csv', 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        existing_data = [row for row in reader]

    filtered_data = [row for row in data if row not in existing_data]

    # 將資料附加到現有的 CSV 檔案中，指定 UTF-8 編碼
    with open('artists.csv', 'a', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        for row in filtered_data:
            writer.writerow(row)

print("爬蟲完成！已將資料附加到 artists.csv 檔案中。")
