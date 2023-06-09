import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd

# 讀取 artists_all.csv 檔案
with open('artists_all.csv', 'r', encoding='ANSI') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # 跳過標題列
    data = list(reader)

# 儲存爬取的資料的列表
result = []

# 計數器
count = 0

# 逐一處理每位歌手的網址
for artist in data:
    artist_name = artist[0]
    artist_url = artist[1]

    # 加上前綴詞"https://mojim.com/"
    full_url = "https://mojim.com/" + artist_url

    try:
        # 發送 GET 請求並獲取網頁內容
        response = requests.get(full_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 尋找每首歌的相關資訊
        song_tags = soup.find_all('span', class_='hc3')
        for tag in song_tags:
            song_a_tags = tag.find_all('a')
            for song_a_tag in song_a_tags:
                song_url = song_a_tag['href']
                song_title = song_a_tag['title']

                # 檢查是否與 songs.csv 中的資料重複
                duplicate_found = False
                with open('songs.csv', 'r', encoding='utf-8-sig') as csvfile:
                    reader = csv.reader(csvfile)
                    next(reader)  # 跳過標題列
                    for row in reader:
                        if row[0] == artist_name and row[1] == song_title:
                            duplicate_found = True
                            break
                
                # 如果沒有重複則加入結果列表
                if not duplicate_found:
                    result.append([artist_name, song_title, song_url])
                
                # 更新計數器
                count += 1

                # 每完成 100 筆資料，將結果附加到 CSV 檔案中
                if count % 100 == 0:
                    df = pd.DataFrame(result, columns=['歌手', '歌曲', '網址'])
                    df.to_csv('songs.csv', mode='a', index=False, header=False, encoding='utf-8')
                    result = []

    except Exception as e:
        # 印出出錯的歌手名稱
        print("爬取", artist_name, "的資料時出現錯誤:", str(e))
        continue

# 檢查是否還有剩餘資料需要附加到 CSV 檔案中
if result:
    df = pd.DataFrame(result, columns=['歌手', '歌曲', '網址'])
    df.to_csv('songs.csv', mode='a', index=False, header=False, encoding='utf-8')

# 印出已完成的歌手名稱
print("所有歌手的資料爬取完成")
