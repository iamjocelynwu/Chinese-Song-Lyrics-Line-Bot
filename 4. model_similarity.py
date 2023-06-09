import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os.path
import jieba
import random

# 設定向量化器和資料存檔路徑
vectorizer_files = ['lyrics_vectorizer.pkl', 'title_vectorizer.pkl', 'singer_vectorizer.pkl']
vector_files = ['lyrics_vector.pkl', 'title_vector.pkl', 'singer_vector.pkl']

# 檢查是否有存檔，若有則載入向量化器和向量資料
if all(os.path.isfile(file) for file in vectorizer_files + vector_files):
    with open(vectorizer_files[0], 'rb') as f:
        lyrics_vectorizer = pickle.load(f)
    with open(vectorizer_files[1], 'rb') as f:
        title_vectorizer = pickle.load(f)
    with open(vectorizer_files[2], 'rb') as f:
        singer_vectorizer = pickle.load(f)
    with open(vector_files[0], 'rb') as f:
        lyrics_vector = pickle.load(f)
    with open(vector_files[1], 'rb') as f:
        title_vector = pickle.load(f)
    with open(vector_files[2], 'rb') as f:
        singer_vector = pickle.load(f)
    data = pd.read_csv('my_final_complete_data.csv', encoding='utf-8')
else:
    data = pd.read_csv('my_final_complete_data.csv', encoding='utf-8')
    data['歌詞'] = data['歌詞'].apply(lambda x: " ".join(jieba.cut(x)))
    data['歌曲名'] = data['歌曲名'].apply(lambda x: " ".join(jieba.cut(x)))
    data['歌手'] = data['歌手'].apply(lambda x: " ".join(jieba.cut(x)))

    lyrics_vectorizer = TfidfVectorizer()
    title_vectorizer = TfidfVectorizer()
    singer_vectorizer = TfidfVectorizer()
    
    #fit_transform()方法是用來訓練TF-IDF向量化器並將文本資料轉換成TF-IDF向量。在訓練階段，我們需要提供整個文本資料集來學習詞彙和計算詞彙的IDF值，因此在這裡我們將整個'歌手'列（這是一個pandas Series）轉換成unicode字符串格式（.values.astype('U')）。這麼做是因為當pandas Series包含非字符串（如NaN或其他Python對象）時，將其轉換成unicode可以確保TF-IDF向量化器可以正確地處理。
    
    lyrics_vector = lyrics_vectorizer.fit_transform(data['歌詞'].values.astype('U'))
    title_vector = title_vectorizer.fit_transform(data['歌曲名'].values.astype('U'))
    singer_vector = singer_vectorizer.fit_transform(data['歌手'].values.astype('U'))

    with open(vectorizer_files[0], 'wb') as f:
        pickle.dump(lyrics_vectorizer, f)
    with open(vectorizer_files[1], 'wb') as f:
        pickle.dump(title_vectorizer, f)
    with open(vectorizer_files[2], 'wb') as f:
        pickle.dump(singer_vectorizer, f)
    with open(vector_files[0], 'wb') as f:
        pickle.dump(lyrics_vector, f)
    with open(vector_files[1], 'wb') as f:
        pickle.dump(title_vector, f)
    with open(vector_files[2], 'wb') as f:
        pickle.dump(singer_vector, f)

def recommend_songs(query):
    query = query.lower()
    if query in data['歌手'].values:
        songs = data[data['歌手'] == query].sample(3, random_state=None)
        return songs.to_dict(orient='records')
  
    query_lyrics = " ".join(jieba.cut(query))
    query_title = " ".join(jieba.cut(query))
    query_singer = " ".join(jieba.cut(query))

#在進行推薦時，我們的查詢（query_singer）已經是一個字符串。在這種情況下，我們只需要用已經訓練過的向量化器來轉換查詢，並不需要再進行.values.astype('U')的操作。這是因為我們已經知道這是一個字符串，並且我們只轉換一個單獨的查詢，而不是整個文本資料集。
#fit_transform()：這個函數首先調用fit()方法來學習模型的參數（例如，資料的均值、標準差、最大最小值等），然後再將這些參數應用到數據集上，進行轉換（例如標準化、正則化等）。所以#fit_transform()是學習參數（fit）以及基於所學參數進行轉換（transform）的一個整合函數。
#transform()：這個函數使用在之前的fit()方法中學習到的參數，來對給定數據進行轉換。transform()方法只進行轉換。
#這兩個方法的主要區別在於，fit_transform()既學習參數也進行轉換，而transform()僅僅進行轉換。
#這在訓練數據與測試數據的處理上有一個重要的應用：在訓練數據上我們應該使用fit_transform()方法，因為我們需要學習數據的參數並將它們應用在數據上。而在測試數據上，我們只需要使用transform()方法，用訓練數據學習到的參數來進行轉換。
    query_lyrics_vector = lyrics_vectorizer.transform([query_lyrics])
    query_title_vector = title_vectorizer.transform([query_title])
    query_singer_vector = singer_vectorizer.transform([query_singer])

    lyrics_similarities = cosine_similarity(query_lyrics_vector, lyrics_vector).flatten()
    title_similarities = cosine_similarity(query_title_vector, title_vector).flatten()
    singer_similarities = cosine_similarity(query_singer_vector, singer_vector).flatten()

    total_similarities = lyrics_similarities * 0.3 + title_similarities * 0.4 + singer_similarities * 0.3

    sorted_indices = total_similarities.argsort()[::-1]
    top3_songs = data.iloc[sorted_indices[:3]].copy()

    def find_matching_lines(lyrics):
        lines = lyrics.split()
        matching_indices = [i for i, line in enumerate(lines) if query in line]
        matching_lines = [lines[i] for i in matching_indices]
        # Add the previous and the next line of each matching line
        for i in matching_indices:
            if i > 0:
                matching_lines.append(lines[i-1])
            if i < len(lines) - 1:
                matching_lines.append(lines[i+1])
        return matching_lines[:3]

    top3_songs['matching_lines'] = top3_songs['歌詞'].apply(find_matching_lines)
    top3_songs = top3_songs[top3_songs['matching_lines'].apply(len) > 0].to_dict(orient='records')

    if len(top3_songs) < 3:
        top3_songs.extend(data.sample(3-len(top3_songs), random_state=None).to_dict(orient='records'))

               
    return top3_songs



def process_input(input_text):
    recommended_songs = recommend_songs(input_text)
    output = []
    for song in recommended_songs:
        song_output = f"歌手: {song['歌手']}\n歌名: {song['歌曲名']}\n歌曲連結: {song['yt_url']}\n相關歌詞:\n"
        song_output += "\n".join("......" + line + "......" for line in song.get('matching_lines', []))
        output.append(song_output)
    return output
