import pandas as pd


df_sports = pd.read_csv('./crawling_data/steam_sports.csv')
df_simulation = pd.read_csv('./crawling_data/steam_simulation.csv')
df_rpg = pd.read_csv('./crawling_data/steam_role_playing.csv')
df_adv = pd.read_csv('./crawling_data/adventure/reviews_2_adventure.csv', index_col = 0)


df_adv= df_adv.rename(columns={'reviews':'review'})

df_adv.to_csv('./crawling_data/adventure/reviews_2_adventure.csv', index=False)

df_sports.info()
df_simulation.info()
df_rpg.info()
df_adv.info()


