from Reddit.CommentList import CommentList
from Reddit.Post import Post


class PostList:
    """
        Una classe per gestire una lista di post su Reddit.
    """
    __posts : list[Post]
    __iter_counter : int

    def __init__(self):
        """
            Inizializza una nuova lista di post.
        """
        self.__posts = []
        self.__iter_counter = 0

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

    def __iter__(self) -> Post|None:
        """
            Restituisce il post corrente per l'iteratore.
        """
        return self.__posts[self.__iter_counter] if len(self.__posts)>self.__iter_counter else None

    def __next__(self):
        """
            Aumenta il contatore nell'iterazione.
        RAISE:
            StopIteration: Se non ci sono più post da iterare.
        """
        if self.__iter_counter == len(self.__posts):
            raise StopIteration

        self.__iter_counter += 1

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
