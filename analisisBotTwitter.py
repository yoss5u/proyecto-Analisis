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