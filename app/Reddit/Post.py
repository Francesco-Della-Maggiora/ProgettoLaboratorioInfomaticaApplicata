from datetime import datetime

from Reddit.CommentList import CommentList
from Reddit.Comment import Comment

class Post:
    """
        Rappresenta un post su Reddit.
    """
    __title : str
    __text : str
    __datetime : datetime
    __comment_list : CommentList

    def __init__(self, title : str, text : str, datetime : datetime, comment_list : CommentList = CommentList()):
        """
            Inizializza un post con il titolo, il testo, la data di pubblicazione e una lista di commenti.
        PARAMETRI:
            title (str): Il titolo del post.
            text (str): Il testo del post.
            datetime (datetime): La data di pubblicazione del post.
            comment_list (CommentList): La lista di commenti associati al post (default è una lista vuota).
        """
        self.__title = title
        self.__text = text
        self.__datetime = datetime
        self.__comment_list = comment_list

    @property
    def title(self) -> str:
        """
            Restituisce il titolo del post.
        RETURNS:
            str: Il titolo del post.
        """
        return self.__title

    @property
    def text(self) -> str:
        """
            Restituisce il testo del post.
        RETURNS:
            str: Il testo del post.
        """
        return self.__text

    @property
    def datetime(self) -> datetime:
        """
            Restituisce la data di pubblicazione del post.
        RETURNS:
            datetime: La data di pubblicazione del post.
        """
        return self.__datetime

    @property
    def comment_list(self) -> CommentList:
        """
            Restituisce la lista dei commenti associati al post.
        RETURNS:
            CommentList: La lista dei commenti associati al post.
        """
        return self.__comment_list

    def append_comment(self, comment : Comment):
        """
            Aggiunge un commento alla lista dei commenti del post.
        PARAMETRI:
            comment (Comment): Il commento da aggiungere alla lista dei commenti del post.
        """
        self.__comment_list.append(comment)
        
    def to_dict(self) -> dict:
        """
            Converte il post in un dizionario.
        RETURNS:
            dict: Un dizionario contenente il titolo, il testo, la data di pubblicazione e la lista dei commenti del post.
        """
        return {
            "title": self.__title,
            "text": self.__text,
            "datetime": self.__datetime.isoformat(),
            "comments": [comment.to_dict() for comment in self.__comment_list]
        }

    def __repr__(self): 
        """
            Restituisce una rappresentazione testuale del post, inclusi titolo, data di pubblicazione, testo e commenti.
        RETURNS:
            str: Rappresentazione del post.
        """
        return f"Titolo: {self.__title}\nData di pubblicazione: {self.__datetime}\n" \
            f"Testo: {self.__text}\nCommenti:\n{self.__comment_list}"

    def __lt__(self, other : 'Post') -> bool:
        """
            Confronta due post in base alla data di pubblicazione.
        PARAMETRI:
            other (Post): Il post da confrontare.
        RETURNS:
            bool: True se il post corrente è pubblicato prima di quello passato come parametro, altrimenti False.
        """
        return self.__datetime < other.__datetime
