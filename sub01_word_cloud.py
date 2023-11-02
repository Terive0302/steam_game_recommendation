import pandas as pd
from wordcloud import WordCloud
import collections
import matplotlib.pyplot as plt
from matplotlib import font_manager

font_path = './malgun.ttf'
font_name = font_manager.FontProperties(fname=font_path).get_name()
plt.rc('font', family='NanumBarunGothic')

df = pd.read_csv('./crawling_data/cleaned_one_review.csv')
words = df.iloc[39, 1].split()
print(words)

word_dict = collections.Counter(words)
word_dict = dict(word_dict)
print(word_dict)

wordcloud_img = WordCloud(
    background_color='white', max_words=2000, font_path=font_path
).generate_from_frequencies(word_dict)

plt.figure(figsize=(12,12))
plt.imshow(wordcloud_img, interpolation='bilinear')
plt.axis('off')
plt.show()