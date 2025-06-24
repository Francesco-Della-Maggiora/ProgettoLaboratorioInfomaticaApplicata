from Reddit import Comment

class CommentList:
    """
        La classe CommentList rappresenta una lista di commenti su Reddit.
    """
    __comments : list[Comment]

    def __init__(self):
        """
            Inizializza una nuova lista di commenti.
        """
        self.__comments = []

    def append(self, comment : Comment) -> None:
        """
            Aggiunge un commento alla lista.
        PARAMETRI:
            comment (Comment): Il commento da aggiungere alla lista.
        """
        self.__comments.append(comment)

    def sort(self, reverse : bool = False) -> None:
        """
            Ordina i commenti nella lista in base alla data di pubblicazione.
        PARAMETRI:
            reverse (bool): Se True, ordina in ordine decrescente, altrimenti in ordine crescente (default False).
        """
        self.__comments.sort(reverse=reverse)

    def __iter__(self):
        return iter(self.__comments)

    def __repr__(self) -> str:
        """
            Restituisce una rappresentazione testuale della lista di commenti, gestendola come l'unione di tutti i commenti.
        RETURNS:
            str: Rappresentazione della lista di commenti.
        """
        return_str = ""

        for comment in self.__comments:
            return_str += str(comment) + "\n"

        return return_str

    def __len__(self) -> int:
        """
            Restituisce il numero di commenti nella lista.
        RETURNS:
            int: Numero di commenti nella lista.
        """
        return len(self.__comments)
