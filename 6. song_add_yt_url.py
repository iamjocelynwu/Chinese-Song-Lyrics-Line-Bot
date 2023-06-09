import pandas as pd
from youtube_search import YoutubeSearch

# 讀取資料
data = pd.read_csv('lyrics_remove_duplicate.csv')

# 創建新欄位
data['yt_url'] = ''

# 定義每次處理的資料筆數
batch_size = 100

# 計算需要處理的迴圈次數
num_batches = len(data) // batch_size + 1

# 進行查詢並更新 yt_url 欄位
for batch in range(num_batches):
    start_idx = batch * batch_size
    end_idx = min((batch + 1) * batch_size, len(data))

    batch_data = data[start_idx:end_idx]

    for index, row in batch_data.iterrows():
        singer = row['歌手']
        song_name = row['歌曲名']

        # 在 Youtube 搜尋影片網址
        results = YoutubeSearch(f'{song_name} {singer}', max_results=1).to_dict()

        if results:
            video_url = 'https://www.youtube.com' + results[0]['url_suffix']
            data.at[index, 'yt_url'] = video_url

    # 每處理完一批資料就保存到 CSV 檔案
    data[start_idx:end_idx].to_csv('lyrics_remove_duplicate.csv', index=False, mode='a', header=(batch == 0))

# 最終保存一次整個資料集
data.to_csv('lyrics_remove_duplicate.csv', index=False)
