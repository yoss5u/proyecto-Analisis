from tkinter import *
from tkinter import messagebox
import tkinter
from analisisBotTwitter import *
from matplotlib.pyplot import text
import pandas as pd 

class MainFrame(Frame):
    
    def __init__(self):

        #parametros a clase de analisis
        dataFrame = pd.read_csv("data.csv")
        dataFrame2 = pd.read_csv("dataelon.csv")
        graphs = informationGraphs(dataFrame, dataFrame2)
        graphs.organizeInformation()
       
        #configuracion ventana Principal
        windowAnalysis = Tk()
        windowAnalysis.geometry('800x600')
        windowAnalysis.configure(background='white')
        windowAnalysis.title('Proyecto Analisis de Datos')
        windowAnalysis.resizable(width=False, height=False)
        
        #configuracion Labels principales
        lblTitulo = Label(windowAnalysis, text="Graficas de Analisis", background='white', font=('Arial', 20), foreground='black').pack()

        #configuracion Botones principales
        btnDynamic = Button(windowAnalysis, text='Grafica sobre cantidad de tweet por fechas', command=graphs.dynamicGraph, border=0)
        btnDynamic.place(x=60, y=100, width=300, height=50)

        btnGraphByLenguage = Button(windowAnalysis, text='Grafica tweets enviador por lenguaje', command=graphs.graphByLenaguage, borderwidth=0)
        btnGraphByLenguage.place(x=60, y=170, width=300, height=50)

        btnGraphBySource = Button(windowAnalysis, text='Grafica tweets enviador por Dispositivo', command=graphs.graphBySource, borderwidth=0)
        btnGraphBySource.place(x=60, y=240, width=300, height=50)

        btnGraphByWords = Button(windowAnalysis, text='Palabras mas utilizadas', command=graphs.showWords, borderwidth=0)
        btnGraphByWords.place(x=440, y=100, width=300, height=50)

        btnGraphHeatMap = Button(windowAnalysis, text='Mapa de calor de cuentas establecidas', command=graphs.mapHeat, borderwidth=0)
        btnGraphHeatMap.place(x=440, y=170, width=300, height=50)

        
        btnGraphHeatMap = Button(windowAnalysis, text='Mostrar DataFrame', command=visualizarDataFrame, borderwidth=0)
        btnGraphHeatMap.place(x=440, y=240, width=300, height=50)

        #inicio ventana principales
        windowAnalysis.mainloop()

def visualizarDataFrame():
    df = pd.read_csv("data.csv")
    app = QApplication(sys.argv)
    model = pandasModel(df)
    view = QTableView()
    view.setModel(model)
    view.resize(800, 600)
    view.show()
    sys.exit(app.exec_()) 

myApp = MainFrame()