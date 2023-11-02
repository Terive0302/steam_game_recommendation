import datetime
import pandas as pd
import glob



# data_path = glob.glob('crawling_data/backup/steam_simulation_*.csv')
# data_path = glob.glob('crawling_data/sports/steam*.csv')
# data_path = glob.glob('crawling_data/rpg/steam*.csv')
# data_path = glob.glob('crawling_data/strategy/steam*.csv')
# data_path = glob.glob('crawling_data/action/steam*.csv')
# data_path = glob.glob('crawling_data/adventure/*.csv')

data_path = glob.glob('crawling_data/steam*.csv')



print(data_path)

df = pd.DataFrame()

for path in data_path:
    df_temp = pd.read_csv(path)
    df_temp.dropna(inplace=True)
    df_temp.drop_duplicates(inplace=True)
    df = pd.concat([df, df_temp], ignore_index=True)
df.drop_duplicates(inplace=True)
df.info()

# df.to_csv('./crawling_data/steam_simulation.csv', index=False)
# df.to_csv('./crawling_data/steam_sports.csv', index=False)
# df.to_csv('./crawling_data/steam_role_playing.csv', index=False)
# df.to_csv('./crawling_data/steam_strategy.csv', index=False)
# df.to_csv('./crawling_data/steam_action.csv', index=False)
# df.to_csv('./crawling_data/steam_adventure.csv', index=False)


df.to_csv('./crawling_data/steam_review_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')), index=False)
