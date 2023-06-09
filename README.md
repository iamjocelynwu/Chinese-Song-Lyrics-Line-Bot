聊歌BOT--想聽什麼歌(詞)?推歌給您
What Chinese lyrics do you want to listen to? Let me recommend some songs for you.

(課程小作業，很low我知道，就當練習嘛!)
This is a small assignment, I know it's not much, but let's consider it as practice!

一、功能介紹 Introduction

1. 收錄範圍：魔鏡歌詞網熱門華語男女歌手240位，共28,208首歌。
Scope: Includes 240 popular Chinese male and female singers from Mojim.com, with a total of 28,208 songs.

2. 輸入想聽的歌詞，「聊歌bot」將推薦３首包含輸入詞的歌曲或歌詞，並提供：歌手、歌曲名、相關歌詞、Youtube影片網址。
Enter the lyrics you want to listen to, and my line bot will recommend 3 songs or lyrics that contain the input words. It will provide the artist, song title, related lyrics, and the YouTube video URL.

3. 也可輸入歌手名，「聊歌bot」隨機推薦該歌手的３首歌給您。
You can also enter the name of an artist, and line bot will randomly recommend 3 songs by that artist.

4. 若找不到相關歌曲，也會隨機推薦３首歌喔！
If no relevant songs are found, it will still recommend 3 random songs!

二、程式說明 Program Explanation
(一)爬蟲與資料處理 Web Scraping and Data Processing
1. 爬取魔鏡歌詞網熱門華語男女歌手名字與專頁網址，存成artists.csv(歌手、專頁網址)
Scrape the names of popular Chinese male and female singers and their respective page URLs from the Mojim.com, and save them as artists.csv (artist, page URL).

2. 讀取artists.csv中第2欄上述專頁網址，爬取該歌手的每首歌名，以及每首歌詞的網址。再另存成songs.csv(歌手、歌曲名、歌詞網址)
Read the above-mentioned page URLs from the 2nd column of artists.csv, scrape the song titles and the URLs of each song's lyrics by those artists. Save them as songs.csv (artist, song title, lyrics URL).

3. 讀取songs.csv每首歌詞的網址，抓取歌詞，存回songs.csv
Read the URLs from songs.csv, fetch the lyrics, and save them back to songs.csv.

4. 針對每個row去重複、去除有出現空白欄位者。針對歌詞，盡量移除雜訊，經歷一系列資料處理(可惜歌詞中出現作詞、作曲人以及贅字變化太多，無法清乾淨)(我大概分了幾次處理，有點忘記散落在那些檔案，程式檔案就不附上來了)，產出lyrics_remove_duplicate.csv
Remove duplicate rows and empty fields in each row. For lyrics, perform a series of data processing to remove noise (unfortunately, there are too many variations in lyricists, composers, and redundant words, so it can't be completely cleaned up). The resulting file is lyrics_remove_duplicate.csv.

5. 使用youtube-search套件中的YoutubeSearch函式，以歌手、歌曲名找尋Youtube歌曲影片網址。新增欄位並存回lyrics_remove_duplicate.csv
Use the YoutubeSearch function from the youtube-search package to search for YouTube video URLs based on the artist and song title. Add a new field and save it back to lyrics_remove_duplicate.csv.

(二)針對輸入詞進行相似度計算 Similarity Calculation for Input Words
1. 將整理完畢的乾淨資料檔，改為my_final_complete_data.csv
Rename the cleaned data file as my_final_complete_data.csv.

2. 讀取上述檔案，將歌詞、歌曲名、歌手利用jieba進行斷詞，各自用空格連接。 
Read the above file and use jieba to tokenize the lyrics, song titles, and artist names, joining each token with a space.

3. 使用TfidfVectorizer().fit_transform()，將歌詞、歌曲名、歌手進行TF-IDF向量化，存成pickle檔，方便每次載入使用。
Use TfidfVectorizer().fit_transform() to vectorize the lyrics, song titles, and artist names using TF-IDF and save them as pickle files for easy loading and use.

4. 優先查詢輸入詞是否為歌手名，如果是，隨機挑3首該歌手的歌推薦。
First, check if the input word is an artist name. If it is, randomly select 3 songs by that artist for recommendation.

5. 若非歌手名稱，將輸入詞斷詞，以空白為前綴。 
If it's not an artist name, tokenize the input word using spaces as prefixes.

6. 使用餘弦相似度（Cosine Similarity）計算輸入詞與每一首曲子(歌詞0.3、歌曲名0.4歌、歌手0.3)的相似度並排序，取出前3名相似度最高者。
Use cosine similarity to calculate the similarity between the input word and each song (lyrics 0.3, song title 0.4, artist 0.3), then sort them and take the top 3 with the highest similarity.

7. 再針對前3名歌曲中，取出有包含之歌詞片段，進行擷取(將歌詞split，然後找出包含輸入詞index，並將其前1行和後1行，return最多3行歌詞。
For the top 3 songs, extract the lyrics snippets that contain the input words (split the lyrics, find the indices of the input words, and return the 1 line before and after each occurrence, up to a maximum of 3 lines).

8. 將歌手、歌曲名、歌詞片段和 YouTube 網址組合成字典。每個字典代表1首歌曲，輸出：歌手、歌曲名、歌詞片段、Youtube網址。輸出成果。
Combine the artist, song title, lyrics snippet, and YouTube URL into a dictionary. Each dictionary represents one song. Output: artist, song title, lyrics snippet, YouTube URL. Output the results.

(三)使用ngrok作為上述相似度比較程式與line的中介，接收line傳來的詞作為上述程式的input，再output程式運作後的結果。這部分不提供程式碼。
Using ngrok as an intermediary between the similarity comparison program and Line, receive the words sent by Line as input to the program, and output the results after the program runs. The code for this part is not provided.

三、舉例 Examples (must type in Chinese because most songs are all "Chinese")
1. (杰倫)(當然你也可以key周杰倫) Jay Chou
![image](https://github.com/iamjocelynwu/Chinese-Song-Lyrics-Line-Bot/assets/98579075/aca6a3cf-8088-4bb2-bda4-d6f44f3cf0ee)

2. 梁靜茹 Fish Leong
![image](https://github.com/iamjocelynwu/Chinese-Song-Lyrics-Line-Bot/assets/98579075/aa693954-287e-4ff8-9822-1e819a8cde2b)

3. 累死 
![image](https://github.com/iamjocelynwu/Chinese-Song-Lyrics-Line-Bot/assets/98579075/163d0961-d317-441c-a2eb-7fe230999c2d)

5. 再見
![image](https://github.com/iamjocelynwu/Chinese-Song-Lyrics-Line-Bot/assets/98579075/84aff240-ddd6-4b3c-8169-7eab896df47b)

四、要是想加line使用也OK，但我都是用免費的資源，隨時可能會停用QQ
If you want to use Line, it's okay, but I'm using free resources, so it may be discontinued at any time. QQ

![L_gainfriends_2dbarcodes_GW](https://github.com/iamjocelynwu/Chinese-Song-Lyrics-Line-Bot/assets/98579075/889ccc4f-3a08-4b1d-998c-42d52a88864b)

謝謝閱讀。
Thank you for reading.
