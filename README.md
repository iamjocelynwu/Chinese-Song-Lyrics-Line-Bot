聊歌BOT--想聽什麼歌詞?推歌給您

What Chinese lyrics do you want to listen to? Let me recommend some songs for you.

(課程小作業，很low我知道，就當練習嘛!)

一、功能介紹
1. 收錄範圍：魔鏡歌詞網熱門華語男女歌手240位，共28,208首歌。
2. 輸入想聽的歌詞，「聊歌bot」將推薦３首包含輸入詞的歌曲或歌詞，並提供：歌手、歌曲名、相關歌詞、Youtube影片網址。
3. 也可輸入歌手名，「聊歌bot」隨機推薦該歌手的３首歌給您。
4. 若找不到相關歌曲，也會隨機推薦３首歌喔！

二、程式說明
(一)爬蟲與資料處理
1. 爬取魔鏡歌詞網熱門華語男女歌手名字與專頁網址，存成csv(歌手、專頁網址)
2. 讀取artists.csv中第2欄上述專頁網址，爬取該歌手的每首歌名，以及每首歌詞的網址。再另存成csv(歌手、歌曲名、歌詞網址)
3. 讀取songs.csv每首歌詞的網址，抓取歌詞，再另存成csv
4. 使用youtube-search套件中的YoutubeSearch函式，以歌手、歌曲名找尋Youtube歌曲影片網址。新增欄位並存回原csv
5. 針對每個row去重複、去除有出現空白欄位者。針對歌詞，盡量移除雜訊(可惜歌詞中出現作詞、作曲人以及贅字變化太多，無法清乾淨)。

(二)針對輸入詞進行相似度計算
1. 將「歌詞」、「歌曲名」、「歌手」利用jieba進行斷詞，各自用空格連接。 
2. 使用TfidfVectorizer().fit_transform()，將「歌詞」、「歌曲名」、「歌手」進行TF-IDF向量化，存成pickle檔，方便每次載入使用。
3. 優先查詢輸入詞是否為歌手名，如果是，隨機挑3首該歌手的歌推薦。
4. 若非歌手名稱，將輸入詞斷詞，以空白為前綴。 
5. 使用餘弦相似度（Cosine Similarity）計算輸入詞與每一首曲子(歌詞0.3、歌曲名0.4歌、歌手0.3)的相似度並排序，取出前3名相似度最高者。
6. 再針對前3名歌曲中，取出有包含之歌詞片段，進行擷取(將歌詞split，然後找出包含輸入詞index，並將其前1行和後1行，return最多3行歌詞。
7. 將歌手、歌曲名、歌詞片段和 YouTube 網址組合成字典。每個字典代表1首歌曲，輸出：歌手、歌曲名、歌詞片段、Youtube網址。輸出成果。

(三)使用ngrok作為上述相似度比較程式與line的中介，接收line傳來的詞作為上述程式的input，再output程式運作後的結果。這部分不提供程式碼。

三、舉例
1. (杰倫)(當然你也可以key周杰倫)
![image](https://github.com/iamjocelynwu/Chinese-Song-Lyrics-Line-Bot/assets/98579075/aca6a3cf-8088-4bb2-bda4-d6f44f3cf0ee)

2. 梁靜茹
![image](https://github.com/iamjocelynwu/Chinese-Song-Lyrics-Line-Bot/assets/98579075/aa693954-287e-4ff8-9822-1e819a8cde2b)

3. 累死
![image](https://github.com/iamjocelynwu/Chinese-Song-Lyrics-Line-Bot/assets/98579075/163d0961-d317-441c-a2eb-7fe230999c2d)

5. 再見
![image](https://github.com/iamjocelynwu/Chinese-Song-Lyrics-Line-Bot/assets/98579075/84aff240-ddd6-4b3c-8169-7eab896df47b)

四、要是想加line使用也OK，但我都是用免費的資源，隨時可能會停用QQ
![L_gainfriends_2dbarcodes_GW](https://github.com/iamjocelynwu/Chinese-Song-Lyrics-Line-Bot/assets/98579075/889ccc4f-3a08-4b1d-998c-42d52a88864b)

謝謝閱讀。
