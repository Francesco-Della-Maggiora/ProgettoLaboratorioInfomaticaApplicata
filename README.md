# Progetto finale del corso "Laboratorio di Informatica Applicata"

Questo progetto permette di analizzare il sentimento dei post e dei commenti di un subreddit su Reddit, visualizzando i risultati tramite grafici.

## Struttura del progetto

- `app/`: codice principale dell'applicazione Flask.
  - `Reddit/`: classi per la gestione di post, commenti e interazione con le API di Reddit.
  - `SentimentAnalysis/`: classi per l'analisi del sentiment e la generazione dei grafici.
  - `static/` e `templates/`: risorse statiche e template HTML per l'interfaccia web.
- `requirements.txt`: dipendenze Python.
- `dockerfile`, `docker-compose.yml`: per esecuzione in ambiente Docker.

## Configurazione

Per aggiungere i file di configurazione occore scaricare la cartella conf e posizionarna all'interno della cartella app, come descritto nella 
<<<<<<< HEAD
[documentazione](#Documentazione)
=======
[#documentazione](documentazione)
>>>>>>> bca81d320f3b5744d5e10aacf7583de92135a217

## Avvio dell'applicazione

1. Costruisci e avvia i container:
   ```
   docker-compose up --build
   ```
2. Accedi all'applicazione su [http://localhost:5000](http://localhost:5000)

## Utilizzo

- Inserisci il nome di un subreddit nella home page.
- Personalizza i parametri avanzati (numero di post, intervalli, titoli grafici, dimensioni assi).
- Visualizza i grafici generati

## API
 
```
- /api/analyze
```
<<<<<<< HEAD
Consente di eseguire un'analisi sui post e i commenti di un determinato subreddit. <br>
Il parametro obbligatorio è subreddit_name che contiene il nome del subreddit su cui fare l'analisi. <br>
L'API accetta anche un parametro opzionale limit (Defualt 10) che indica il numero di post su cui fare l'analisi. Se il valore di limit è minore o uguale di 0 viene preso in considerazione il valore di Default.

Esempio:
```
/api/analyze?subreddit_name=python&limit=1
```
Risposta
```
{ "2025-06-28T13:57:13+00:00": { "Negativo": 0, "Neutrale": 0, "Positivo": 1 } }
```
=======
Consente di eseguire un'analisi sui post e i commenti di un determinato subreddit. 
Il parametro obbligatorio è subreddit_name che contiene il nome del subreddit su cui fare l'analisi.
Parametro opzionale limit (Defualt 10) che indica il numero di post su cui fare l'analisi. Se il valore di limit è minore o uguale di 0 viene preso in considerazione il valore di Default.

Esempio:
/api/analyze?subreddit_name=python&limit=1
Risposta
{ "2025-06-28T13:57:13+00:00": { "Negativo": 0, "Neutrale": 0, "Positivo": 1 } }
>>>>>>> bca81d320f3b5744d5e10aacf7583de92135a217

## Documentazione

- Nel branch Doc sono è presente il notebook "ReportDellaMaggiora" che contiene la documentazione del progetto
