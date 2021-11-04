import math
import pandas as pd
from pandas.core.frame import DataFrame
from pandas.core.groupby.groupby import GroupByPlot #Manipulacion de datos
import seaborn as sns #Visualizacion de datos
import matplotlib.pyplot as plt #Realizar graficos
from wordcloud import WordCloud, STOPWORDS
import numpy as np
import sys
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt


class informationGraphs():
    def __init__(self, dataFrame1, dataFrame2) -> None:
        self.dataFrameIbai = dataFrame1
        self.dataFrameElon = dataFrame2
    
    def organizeInformation(self):
        #Separar la fecha creacion de la cuenta de usuario por dia, mes y aÃ±o 
        self.dataFrameIbai['user_created_profile'] = pd.to_datetime(self.dataFrameIbai['user_created_profile'])
        self.dataFrameIbai['YearUser'] = self.dataFrameIbai['user_created_profile'].dt.year
        self.dataFrameIbai['DayUser'] = self.dataFrameIbai['user_created_profile'].dt.day
        self.dataFrameIbai['MonthUser'] = self.dataFrameIbai['user_created_profile'].dt.month
    
        self.dataFrameIbai['date'] = pd.to_datetime(self.dataFrameIbai['date'], format="%d-%m-%Y")
        self.dataFrameIbai.sort_values(by='date', ascending=False)
        self.dataFrameIbai['date'] = self.dataFrameIbai['date'].dt.strftime("%d-%m-%Y")

        #Obtiene datos estadisticos del DataFrame
        describeInfo = self.dataFrameIbai.describe()

    def dynamicGraph(self):
        groupBySource = self.dataFrameIbai.groupby('date')['_id'].count().to_dict()
        print((groupBySource))
        plt.axis([0, 49, 0, 20000])
        plt.xticks(rotation=45, visible=True)
        plt.ion()

        xs = [0, 0]
        ys = [0, 0]
        x = 0
        for i in groupBySource:
            y = groupBySource[i]
            xs[0] = xs[1]
            ys[0] = ys[1]
            xs[1] = i
            ys[1] = y
            plt.plot(xs, ys)
            plt.pause(0.1)
            x += 1
            print(x)

    def graphByLenaguage(self):
        categoricalVariables = ['lenguage']
        for catVar in categoricalVariables:
            frequency = self.dataFrameIbai[catVar].value_counts()
            df_frequency = pd.DataFrame({'Idiomas detectados': frequency.index.tolist(), 'Cantidad de tweets':frequency.tolist()
            })
            sns.barplot(x='Idiomas detectados', y='Cantidad de tweets', data=df_frequency.head(10))
            plt.xticks(rotation=90, visible=True)
            plt.show()


    def graphBySource(self):
        data = self.dataFrameIbai
        df = data.groupby(['source']).size().to_frame('count').sort_values(['count'], ascending=False).head(10)
        print(df)
        ax = df.plot(kind='barh', figsize=(20, 9), color='#86bf91', zorder=2, width=0.85)
        # Despine
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        # Switch off ticks
        ax.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off",
                    labelleft="on")
        # Draw vertical axis lines
        vals = ax.get_xticks()
        for tick in vals:
            ax.axvline(x=tick, linestyle='dashed', alpha=0.4, color='#eeeeee', zorder=1)
        # Set x-axis label
        ax.set_xlabel("Total", labelpad=20, weight='bold', size=12)
        # Set y-axis label
        ax.set_ylabel("Source", labelpad=20, weight='bold', size=12)
        # Plot
        plt.show()


    def mapHeat(self):
        data = self.dataFrameIbai
        data['user_created_profile'] = pd.to_datetime(data['user_created_profile'], format='%d-%m-%Y')
        data['day'] = data['user_created_profile'].dt.day
        data['month'] = data['user_created_profile'].dt.month
        data['year'] = data['user_created_profile'].dt.year
        df = data.groupby(['year', 'month']).size().to_frame('count').sort_values(['count'], ascending=False).reset_index()
        print(df)
        pivot = df.pivot(index='year', columns='month', values='count')
        sns.set()
        ax = sns.heatmap(pivot)
        plt.xticks(rotation=-90)
        plt.show()
        

    def comparationLenguage(self):
        df = self.dataFrameIbai.groupby(['source']).size().to_frame('Total_Ibai').sort_values(['Total_Ibai'], ascending=False).head(10).reset_index()
        df2 = self.dataFrameElon.groupby(['source']).size().to_frame('Total_Elon').sort_values(['Total_Elon'], ascending=False).head(10).reset_index()
        df3 = pd.merge(df, df2, on='source')

        df3.plot.bar(x='source')
        plt.xticks(rotation=0)
        plt.legend()
        plt.show()

    def comparationCountry(self):
        df = self.dataFrameIbai.groupby(['lenguage']).size().to_frame('Total_Ibai').sort_values(['Total_Ibai'], ascending=False).head(10).reset_index()
        df2 = self.dataFrameElon.groupby(['lenguage']).size().to_frame('Total_Elon').sort_values(['Total_Elon'], ascending=False).head(10).reset_index()
        df3 = pd.merge(df, df2, on='lenguage')

        df3.plot.bar(x='lenguage')
        plt.xticks(rotation=0)
        plt.legend()
        plt.show()

    def showWords(self):
        data = self.dataFrameIbai
        data_head = data.head(20)
        print(data_head)
        text = " ".join(review for review in data.text_tweet)
        print("There are {} words in the combination of all review.".format(len(text)))
        stopwords = set(STOPWORDS)
        stopwords.update(["IbaiLlanos", "https", "t", "co", "y"])
        wordcloud = WordCloud(stopwords=stopwords, background_color="white", width=1500, height=1200).generate(text)

        # Display the generated image:
        # the matplotlib way:
        plt.figure(figsize=(20, 9))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()


class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None