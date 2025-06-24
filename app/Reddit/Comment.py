from datetime import datetime

class Comment:
    """
        Rappresenta un commento su Reddit.
    """
    __text : str
    __datetime : datetime

    def __init__(self, text : str, datetime : datetime):
        """
            Inizializza un commento con il testo e la data di pubblicazione.
        PARAMETRI:
            text (str): Il testo del commento.
            datetime (datetime): La data di pubblicazione del commento.
        """
        self.__text = text
        self.__datetime = datetime

    @property
    def text(self) -> str:
        """
            Restituisce il testo del commento.
        RETURNS:
            str: Il testo del commento.
        """
        return self.__text

    @property
    def datetime(self) -> datetime:
        """
            Restituisce la data di pubblicazione del commento.
        RETURNS:
            datetime: La data di pubblicazione del commento.
        """
        return self.__datetime

    def to_dict(self) -> dict:
        """
            Converte il commento in un dizionario.
        RETURNS:
            dict: Un dizionario contenente il testo e la data di pubblicazione del commento.
        """
        return {
            'text': self.__text,
            'datetime': self.__datetime.isoformat()
        }

    def __repr__(self) -> str:
        """
            Restituisce una rappresentazione testuale del commento.
        RETURNS:
            str: Rappresentazione del commento.
        """
        return f"Data di Pubblicazione: {self.__datetime}, Testo: {self.__text}"

    def __lt__(self, other : 'Comment') -> bool:
        """
            Confronta due commenti in base alla data di pubblicazione.
        PARAMETRI:
            other (Comment): Il commento da confrontare.
        RETURNS:    
            bool: True se il commento corrente è stato pubblicato prima di `other`, altrimenti False.
        """
        return self.__datetime < other.__datetime

    @staticmethod
    def from_dict(data: dict) -> 'Comment':
        """
            Crea un commento da un dizionario.
        PARAMETRI:
            data (dict): Il dizionario contenente il testo e la data di pubblicazione del commento.
        RETURNS:
            Comment: Un'istanza di Comment creata dai dati forniti.
        """
        return Comment(
            text=data['text'],
            datetime=datetime.fromisoformat(data['datetime'])
        )
