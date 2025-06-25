from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import Reddit
import string
import os
import re

class SentimentAnalyzer:
    """
        Classe per l'analisi del sentiment dei post e dei commenti su Reddit.
    """
    @staticmethod
    def translate_sentiment(sentiment : dict) -> str:
        """
            Traduce la label del sentiment nella stringa corrispondente.
        PARAMETRI:
            sentiment (dict): Il dizionario contenente la label del sentiment.
        RETURNS:
            str: La stringa corrispondente alla label del sentiment.
        """
        if sentiment["label"] == "LABEL_0":
            return "Negativo"
        elif sentiment["label"] == "LABEL_1":
            return "Neutrale"
        elif sentiment["label"] == "LABEL_2":
            return "Positivo"
        
        raise ValueError(f"La label {sentiment['label']} non è riconosciuta come una delle etichette previste.")

    def __init__(self, model_path : str = f"{os.path.dirname(__file__)}/../config/finetuning-sentiment-model-reddit-data"):
        """
            Inizializza il SentimentAnalyzer con il modello e il tokenizer specificati.
        PARAMETRI:
            model_path (str): Il percorso del modello pre-addestrato da utilizzare per l'analisi del sentiment (default è il percorso relativo al modello di sentiment analysis).
        """
        self.__tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.__model = AutoModelForSequenceClassification.from_pretrained(model_path, num_labels=3, problem_type="single_label_classification")
        self.__sentiment_analyzer = pipeline("sentiment-analysis", model=self.__model, tokenizer=self.__tokenizer)

    def analyze(self, posts : Reddit.PostList, verbose: bool = True) -> dict:
        """
            Analizza il sentiment dei post e dei commenti in una lista di post.
        PARAMETRI:
            posts (Reddit.PostList): La lista di post da analizzare.
            verbose (bool): Se True, stampa lo stato di avanzamento dell'analisi (default True).
        RETURNS:
            dict: Un dizionario contenente il conteggio dei sentimenti per ogni data di pubblicazione dei post e dei commenti.
        """
        
        results = {}
        len_posts = len(posts)
        for index, post in enumerate(posts):
            text = self.clean_text(post.title + " " + post.text)
            sentiment = self.__sentiment_analyzer(text)

            if post.datetime not in results:
                results[post.datetime] = {
                    "Negativo": 0,
                    "Neutrale": 0,
                    "Positivo": 0
                }

            results[post.datetime][self.translate_sentiment(sentiment[0])] += 1

            for comment in post.comment_list:
                sentiment = self.__sentiment_analyzer(self.clean_text(comment.text))
                if comment.datetime not in results:
                    results[comment.datetime] = {
                        "Negativo": 0,
                        "Neutrale": 0,
                        "Positivo": 0
                    }

                results[comment.datetime][self.translate_sentiment(sentiment[0])] += 1

            if verbose:
                print(f"Analizzato {index + 1}/{len_posts} post ...")
        
        return results

    @staticmethod
    def clean_text(text : str) -> str:
        """
            Pulisce il testo  trasnformandolo in minuscolo, rimuovendo URL, menzioni, hastag, emoji e punteggiatura.
        PARAMETRI:
            text (str): Il testo da pulire.
        RETURNS:
            str: Il testo pulito.
        """
        text = text.lower()
        text = re.sub(r'http\S+|www\.\S+', '', text)
        text = re.sub(r'@\w+', '', text)
        text = re.sub(r'#\w+', '', text)
        emoji_pattern = re.compile(
            "["
            u"\U0001F600-\U0001F64F"  # emoticon
            u"\U0001F300-\U0001F5FF"  # simboli e pittogrammi
            u"\U0001F680-\U0001F6FF"  # trasporti e simboli mappa
            u"\U0001F1E0-\U0001F1FF"  # bandiere
            "]+", flags=re.UNICODE
        )
        text = emoji_pattern.sub(r'', text)
        text = text.translate(str.maketrans('', '', string.punctuation))
        #testo = re.sub(r'\s+', ' ', testo).strip()

        return text
