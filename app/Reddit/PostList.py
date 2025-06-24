from Reddit.CommentList import CommentList
from Reddit.Post import Post
import json

class PostList:
    """
        Una classe per gestire una lista di post su Reddit.
    """
    __posts : list[Post]

    def __init__(self):
        """
            Inizializza una nuova lista di post.
        """
        self.__posts = []

    def append(self, post : Post):
        """
            Aggiunge un post alla lista.
        PARAMETRI:
            post (Post): Il post da aggiungere alla lista.
        """
        self.__posts.append(post)

    def sort(self, reverse=False):
        """
            Ordina i post nella lista in base alla data di pubblicazione.
        PARAMETRI:
            reverse (bool): Se True, ordina in ordine decrescente, altrimenti in ordine crescente (default False).
        """
        self.__posts.sort(reverse=reverse)

    def __iter__(self):
        return iter(self.__posts)

    def __len__(self) -> int:
        """
            Restituisce il numero di post nella lista.
        RETURNS:
            int: Il numero di post nella lista.
        """
        return len(self.__posts)

    def __repr__(self) -> str:
        """
            Restituisce una rappresentazione testuale della lista di post, gestendola come l'unione di tutti i post.
        RETURNS:
            str: Rappresentazione della lista di post.
        """
        return_str = ""

        for post in self.__posts:
            return_str += str(post) + "\n"

        return return_str

    def to_json(self) -> str:
        """
            Converte l'intera lista in una stringa JSON.
        """
        return json.dumps([post.to_dict() for post in self.__posts], ensure_ascii=False, indent=4)