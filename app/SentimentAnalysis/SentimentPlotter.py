from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class SentimentPlotter:

    __labels : list[datetime]
    __negative : list[int]
    __neutral : list[int]
    __positive : list[int]
    __total : list[int]

    def __init__(self, sentiment_data : dict[datetime, dict[str, int]], n_interval : int = 10):
        """
            Inizializza il plotter del sentiment con i dati di sentiment e il numero di intervalli desiderati.
        PARAMETRI:
            sentiment_data (dict): Un dizionario contenente i dati di sentiment, dove le chiavi sono date e i valori sono dizionari 
                    con chiavi "Negativo", "Neutrale" e "Positivo".
            n_interval (int): Il numero di intervalli in cui suddividere i dati di sentiment (Default: 10)
        """
        
        self.__labels = []
        self.__negative = []
        self.__neutral = []
        self.__positive = []
        self.__total = []

        date_keys = list(sentiment_data.keys())
        date_keys.sort() 

        if not date_keys:
            raise ValueError("Il dizionario è vuoto.")

        min_date = date_keys[0]
        max_date = date_keys[-1]

        intervallo_totale = max_date - min_date
        step = intervallo_totale / n_interval

        for i in range(n_interval):
            
            end_interval = min_date + (i + 1) * step            
            if i == 9: #Evita errori di arrotondamento
                end_interval = max_date

            self.__labels.append(end_interval)
            self.__negative.append(0)
            self.__neutral.append(0)
            self.__positive.append(0)
            self.__total.append(0)

            index = 0
            while index < len(date_keys) and date_keys[index] < end_interval:
                self.__negative[-1] += sentiment_data[date_keys[index]]["Negativo"]
                self.__neutral[-1] += sentiment_data[date_keys[index]]["Neutrale"]
                self.__positive[-1] += sentiment_data[date_keys[index]]["Positivo"]
                self.__total[-1] += sentiment_data[date_keys[index]]["Negativo"] + sentiment_data[date_keys[index]]["Neutrale"] + sentiment_data[date_keys[index]]["Positivo"]    
                index += 1

    def plot_sentiment(self, save_path : str = "img/sentiment_plot.png", title : str = "Andamento dei Sentimenti", figsize : tuple[int, int] = (10, 5)):

        for i in range(len(self.__labels)):
            counter = self.__negative[i] + self.__neutral[i] + self.__positive[i]
            self.__negative[i] = (self.__negative[i] / counter) * 100 
            self.__neutral[i] = (self.__neutral[i] / counter) * 100
            self.__positive[i] = (self.__positive[i] / counter) * 100
        
        plt.figure(figsize=figsize)
        plt.plot(self.__labels, self.__negative, label='Negativo', color='red', marker='o')
        plt.plot(self.__labels, self.__neutral, label='Neutrale', color='gray', marker='o')
        plt.plot(self.__labels, self.__positive, label='Positivo', color='green', marker='o')
    
        plt.xticks(rotation=45)
        plt.ylim(0, 100) 
        plt.xlim(self.__labels[0], self.__labels[-1])

        plt.xticks(ticks=self.__labels[::1], labels=[l.strftime('%d-%m-%y\n%H:%M') for l in self.__labels[::1]])

        plt.title(title)
        plt.xlabel('Date in Analisi')
        plt.ylabel('Valori in percentuale')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        plt.savefig(save_path)
    
    def plot_total_posts(self, save_path : str = "img/total_posts_plot.png", title : str = "Andamento dei Post Totali", figsize : tuple[int, int] = (10, 5)):
        """
            Plotta il numero totale di post e commenti nel tempo.
        PARAMETRI:
            save_path (str): Il percorso dove salvare il grafico (Default: "img/total_posts_plot.png")
            title (str): Il titolo del grafico (Default: "Andamento del numero di Post Totali")
            figsize (tuple): La dimensione della figura del grafico (Default: (10, 5))
        """
        plt.figure(figsize=figsize)
        plt.plot(self.__labels, self.__total, color='blue', marker='o')

        plt.xticks(rotation=45)
        plt.ylim(0, self.__total[-1])
        plt.xlim(self.__labels[0], self.__labels[-1])

        plt.xticks(ticks=self.__labels[::1], labels=[l.strftime('%d-%m-%y\n%H:%M') for l in self.__labels[::1]])

        plt.title(title)
        plt.xlabel('Date in Analisi')
        plt.ylabel('Numero di Post e Commenti')
        plt.grid(True)
        plt.tight_layout()

        plt.savefig(save_path)