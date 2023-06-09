import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os.path
import jieba
import random

# 設定向量化資料存檔路徑
vectorizer_files = ['lyrics_vectorizer.pkl', 'title_vectorizer.pkl', 'singer_vectorizer.pkl']
vector_files = ['lyrics_vector.pkl', 'title_vector.pkl', 'singer_vector.pkl']

# 檢查是否有存檔，若有則載入向量資料
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
