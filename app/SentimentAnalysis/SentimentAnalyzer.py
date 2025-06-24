from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import Reddit
import os

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
            sentiment = self.__sentiment_analyzer(post.title + " " + post.text)

            if post.datetime not in results:
                results[post.datetime] = {
                    "Negativo": 0,
                    "Neutrale": 0,
                    "Positivo": 0
                }

            results[post.datetime][self.translate_sentiment(sentiment[0])] += 1

            for comment in post.comment_list:
                sentiment = self.__sentiment_analyzer(comment.text)
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