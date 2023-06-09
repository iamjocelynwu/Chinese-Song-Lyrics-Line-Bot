import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd

# 讀取 songs.csv 檔案
df = pd.read_csv('songs.csv')

# 儲存歌詞的列表
lyric_data = []

# 計數器
count = 0

# 逐行取出'網址'，爬取歌詞並附加到'songs.csv'的第4個欄位中
for index, row in df.iterrows():
    song_url = row['網址']

    # 加上前綴詞"https://mojim.com/"
    full_url = "https://mojim.com/" + song_url

    try:
        # 發送 GET 請求並獲取網頁內容
        response = requests.get(full_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 尋找歌詞結構
        lyric_tag = soup.find('dd', id='fsZx3')
        lyric = lyric_tag.text.strip() if lyric_tag else ""

        # 將歌詞資料加入列表
        lyric_data.append([row['歌手'], row['歌曲'], row['網址'], lyric])

        # 每100首歌曲存一次歌詞到'lyrics.csv'
        count += 1
        if count % 100 == 0:
            df_lyrics = pd.DataFrame(lyric_data, columns=['歌手', '歌曲', '網址', '歌詞'])
            df_lyrics.to_csv('lyrics.csv', mode='a', index=False, header=not count > 100, encoding='utf-8-sig')
            lyric_data = []  # 清空歌詞資料列表

        # 更新歌詞欄位
        df.at[index, '歌詞'] = lyric

    except Exception as e:
        # 印出出錯的歌手名稱
        print("爬取歌手", row['歌手'], "的歌詞時出現錯誤:", str(e))
        continue

# 將最後一批歌詞資料存到'lyrics.csv'
if len(lyric_data) > 0:
    df_lyrics = pd.DataFrame(lyric_data, columns=['歌手', '歌曲', '網址', '歌詞'])
    df_lyrics.to_csv('lyrics.csv', mode='a', index=False, header=not count > 100, encoding='utf-8-sig')

# 儲存修改後的'songs.csv'檔案
df.to_csv('songs.csv', index=False, encoding='utf-8-sig')


print("所有歌詞爬取完成")
