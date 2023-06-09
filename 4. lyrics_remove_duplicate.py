import pandas as pd

# 讀取csv檔案
df = pd.read_csv('lyrics_final_cleaned.csv', encoding='utf-8')

# 去除重複資料
df_unique = df.drop_duplicates(subset=['歌手', '歌曲名'])

# 計算移除的重複資料筆數
removed_duplicates = len(df) - len(df_unique)
print(f"移除了 {removed_duplicates} 筆重複的資料")

# 定義批次寫入csv檔案的函式
def append_to_csv(df, filename):
    df.to_csv(filename, mode='a', header=False, index=False, encoding='utf-8-sig')

# 批次整理資料並寫入新的csv檔案
batch_size = 100
total_rows = len(df_unique)
start_row = 0

output_filename = 'lyrics_remove_duplicate.csv'

while start_row < total_rows:
    end_row = min(start_row + batch_size, total_rows)
    batch_df = df_unique.iloc[start_row:end_row, :].copy()
    
    # 批次寫入新的csv檔案
    if start_row == 0:
        batch_df.to_csv(output_filename, mode='w', index=False, encoding='utf-8-sig')
    else:
        append_to_csv(batch_df, output_filename)
    
    start_row += batch_size
