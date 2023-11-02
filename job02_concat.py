import datetime
import pandas as pd
import glob



data_path = glob.glob('./crawling_data/backup/steam*.csv')
print(data_path)

df = pd.DataFrame()

for path in data_path:
    df_temp = pd.read_csv(path)
    df_temp.dropna(inplace=True)
    df_temp.drop_duplicates(inplace=True)
    df = pd.concat([df, df_temp], ignore_index=True)
df.drop_duplicates(inplace=True)
df.info()

df.to_csv('./crawling_data/steam_review_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')), index=False)
