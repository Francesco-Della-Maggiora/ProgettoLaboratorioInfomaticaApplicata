from flask import Flask, render_template, request, jsonify, send_from_directory
from SentimentAnalysis import SentimentAnalyzer, SentimentPlotter
from Reddit import RedditAPI, PostList
import prawcore
import hashlib
import os

def analyze(request) -> dict|tuple:
    if request.method != 'GET':
        return ({'error': 'Metodo non supportato. Utilizzare GET.'}, 405)
    
    subreddit = request.args.get('subreddit_name')
    if not subreddit:
        return ({'error': 'Il Parametro subreddit è obbligatorio'}, 400)

    limit = request.args.get('limit', 10, type=int)
    if limit <= 0:
        limit = 10
    
    reddit = RedditAPI(f"{os.path.dirname(__file__)}/config/config.json")
    posts : PostList = reddit.get_posts(subreddit, limit=limit)

    if not posts or len(posts) == 0:
        return ({'error': 'Nessun post trovato per il subreddit specificato'}, 404)
            
    sa = SentimentAnalyzer(f"{os.path.dirname(__file__)}/config/finetuning-sentiment-model-reddit-data")
    return sa.analyze(posts, verbose=True)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze')
def analyze_page():
    try:
        results = analyze(request)
        if isinstance(results, tuple):
            text, status_code = results
            return render_template('error.html', error=text), status_code
    except Exception as e:
        if isinstance(e, prawcore.exceptions.NotFound):
            return render_template('error.html', error='Subreddit non trovato'), 404
        elif isinstance(e, prawcore.exceptions.Forbidden):
            return render_template('error.html', error='Accesso negato al subreddit'), 403
        elif isinstance(e, prawcore.exceptions.BadRequest):
            return render_template('error.html', error='Richiesta non valida'), 400
        elif isinstance(e, prawcore.exceptions.ServerError):
            return render_template('error.html', error='Errore del server di Reddit'), 500
        elif isinstance(e, prawcore.exceptions.TooManyRequests):
            return render_template('error.html', error='Troppe richieste, attendere e riprovare'), 429
        elif isinstance(e, prawcore.exceptions.Redirect):
            return render_template('error.html', error='Redirect non supportato'), 301
        
        return render_template('error.html', error=f'Errore durante l\'analisi: {str(e)}'), 500
        
    n_interval = request.args.get('n_interval', 10, type=int)
    if n_interval <= 0:
        n_interval = 10
                
    x_axis = request.args.get('x_axis_size', 15, type=int)
    if x_axis <= 0:
        x_axis = 15
                
    y_axis = request.args.get('y_axis_size', 5, type=int)
    if y_axis <= 0:
        y_axis = 5

    title_sentiment = request.args.get('title1', 'Analisi del Sentiment')
    title_number = request.args.get('title2', 'Numero di post e commenti totali')

    sp = SentimentPlotter(results, n_interval=n_interval)
            
    sentiment = f"{title_sentiment}-{request.args.get('subreddit_name')}-{n_interval}-{x_axis}-{y_axis}-sentiment"
    counter = f"{title_sentiment}-{request.args.get('subreddit_name')}-{n_interval}-{x_axis}-{y_axis}-counter"

    path_sentiment = f"{hashlib.md5(sentiment.encode()).hexdigest()}.png"
    path_counter = f"{hashlib.md5(counter.encode()).hexdigest()}.png"

    sp.plot_sentiment(  save_path=f"{os.path.dirname(__file__)}/generated/{path_sentiment}", title=title_sentiment, figsize=(x_axis, y_axis))
    sp.plot_total_posts(save_path=f"{os.path.dirname(__file__)}/generated/{path_counter}", title=title_number, figsize=(x_axis, y_axis))

    return render_template(
        'results.html',
        sentiment_image=path_sentiment,
        counter_image=path_counter
    )

@app.route('/api/analyze')
def analyze_api():
    try:
        results = analyze(request)
        if isinstance(results, tuple):
            text, status_code = results
            return jsonify({'error': text}), status_code
        return jsonify({k.isoformat(): v for k, v in results.items()})
    
    except Exception as e:
        return jsonify({'error': f'Errore durante l\'analisi: {str(e)}'}), 500

@app.route('/generated/<filename>')
def generated_image(filename):
    return send_from_directory('generated', filename)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
