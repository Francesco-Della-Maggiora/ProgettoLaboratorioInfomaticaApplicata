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

    def to_dict(self) -> list[dict]:
        """
            Converte la lista di post in una lista di dizionari.
        RETURNS:
            list[dict]: Una lista di dizionari, ciascuno rappresentante un post.
        """
        return [post.to_dict() for post in self.__posts]
    
    def save_json(self, json_path : str) -> str:
        """
            Salva la lista di post in un file JSON.
        PARAMETRI:
            json_path (str): Il percorso del file JSON in cui salvare i post.
        """
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=4)    
    
    @staticmethod
    def from_json(json_string: str) -> 'PostList':
        """
            Crea una PostList da una stringa JSON.
        PARAMETRI:
            json_string (str): La stringa JSON da cui creare la PostList.
        RETURNS:
            PostList: Un'istanza di PostList popolata con i dati dalla stringa JSON.
        """
        post_list = PostList()
        with open(json_string, 'r', encoding='utf-8') as f:
            posts_data = json.load(f)

        if len(posts_data) == 0:
            return PostList()

        for post_data in posts_data:
            post = Post.from_dict(post_data)
            post_list.append(post)

        return post_list