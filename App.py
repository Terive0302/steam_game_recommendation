import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from gensim.models import Word2Vec
from scipy.io import mmread
import pickle
from PyQt5.QtCore import QStringListModel
from wordcloud import WordCloud
import collections
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from konlpy.tag import Okt
from PyQt5.QtGui import QPixmap,QImage



form_window = uic.loadUiType('./steam_game_recommendation.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Tfidf_matrix = mmread('./models/tfidf_game_review.mtx').tocsr()
        with open('./models/tfidf.pickle', 'rb') as f:
            self.Tfidf = pickle.load(f)
        self.embedding_model = Word2Vec.load('./models/word2vec_game_review.model')
        self.df_reviews = pd.read_csv('crawling_data/cleaned_one_review.csv')
        self.titles = list(self.df_reviews['titles'])
        self.titles.sort()
        self.btn_recommendation.clicked.connect(self.btn_slot)

        model = QStringListModel()  # 자동 완성
        model.setStringList(self.titles)  # 자동 완성
        completer = QCompleter()  # 자동 완성
        completer.setModel(model)  # 자동 완성
        self.le_keyword.setCompleter(completer)  # 자동 완성



    def btn_slot(self):
        keyword = self.le_keyword.text()
        self.le_keyword.setText('')
        self.lbl_keyword.setText('검색 내용 : '+ keyword)
        if keyword:
            if keyword in self.titles:
                recommendation = self.recommendation_by_game_title(keyword)
                self.lbl_recommendation.setText(recommendation)
            else:
                recommendation = self.recommendation_by_keyword(keyword)
                self.lbl_recommendation.setText(recommendation)

    def recommendation_by_game_title(self, title):
        movie_idx = self.df_reviews[self.df_reviews['titles']==title].index[0]
        cosine_sim = linear_kernel(self.Tfidf_matrix[movie_idx], self.Tfidf_matrix)
        recommendation = self.getRecommendation(cosine_sim)
        return recommendation

    def recommendation_by_keyword(self, keyword):
        okt= Okt()
        df_stopwords = pd.read_csv('./stopwords.csv')
        stopwords = list(df_stopwords['stopword'])
        try:
            token_sentence = okt.pos(keyword, stem=True)
            sentences = []
            sentence_processing = []
            words = []
            for word, _ in token_sentence:
                sentences.append(word)
            for sentence in sentences:
                if len(sentence) > 1:
                    if sentence not in stopwords:
                        sentence_processing.append(sentence)
            for keyword in sentence_processing:
                try:
                    sim_word = self.embedding_model.wv.most_similar(keyword, topn=10)
                    for word, _ in sim_word:
                        words.append(keyword)
                        words.append(word)
                except:
                    return '다른 키워드를 이용하세요.'
            sentence = []
            for word in words:
                sentence = sentence + [word]
            sentence = ' '.join(sentence)
            sentence_vec = self.Tfidf.transform([sentence])
            cosine_sim = linear_kernel(sentence_vec, self.Tfidf_matrix)
            recommendation = self.getRecommendation(cosine_sim)
            return recommendation
        except:
            return '다른 키워드를 이용하세요.'

    def getRecommendation(self, cosine_sim):
        simScore = list(enumerate(cosine_sim[-1]))
        simScore = sorted(simScore, key=lambda x: x[1], reverse=True)
        simScore = simScore[:11]
        movieIdx = [i[0] for i in simScore]
        recMovieList = self.df_reviews.iloc[movieIdx, 0]
        print(movieIdx)
        recMovieList = '\n'.join(recMovieList[1:])
        self.showWordcloud(movieIdx[0])
        self.label2.setText(str(recMovieList.split('\n')[0]))
        return recMovieList

    def showWordcloud(self, movieIdx):
        font_path = './malgun.ttf'
        plt.rc('font', family='NanumBarunGothic')
        df = pd.read_csv('crawling_data/cleaned_one_review.csv')
        words = df.iloc[movieIdx, 1].split()
        word_dict = collections.Counter(words)
        word_dict = dict(word_dict)
        wordcloud_img = WordCloud(
            background_color='white', max_words=2000, font_path=font_path
        ).generate_from_frequencies(word_dict)
        plt.figure(figsize=(6, 12))
        plt.imshow(wordcloud_img, interpolation='bilinear')
        plt.axis('off')
        plt.savefig('./savefig_default.png')
        # plt.show()
        pixmap = QPixmap('./savefig_default.png')
        self.label.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())