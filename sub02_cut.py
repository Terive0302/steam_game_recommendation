import pandas as pd
import os
import glob



filePath = './crawling_data/final/'
fileAll = os.listdir(filePath)

for file in fileAll:
    rowsize = sum(1 for row in (open(filePath + file, encoding='UTF-8')))
    newsize = 60000
    times = 0
    for i in range(1, rowsize, newsize):
        times += 1
        df = pd.read_csv(filePath + file, header=None, nrows=newsize, skiprows=i)
        csv_output = file[:-4] + '_' + str(times) + '.csv'
        df.to_csv(filePath + csv_output, index=False)

data_path = glob.glob('crawling_data/final/steam_review_20231102_*.csv')

df = pd.DataFrame()

for path in data_path:
    df_temp = pd.read_csv(path)
    print(path)
    df_temp = df_temp.rename(columns={'0': 'title', '1':'review'})
    df_temp.to_csv(path, index=False)
