from flask import Flask, render_template, redirect, request, jsonify, session
from flask.helpers import url_for
from requests import get, post
from json import loads
from user.models import User

OMDB_KEY = "8b7aa942"
TMDB_KEY = "70be0504665db30a675274901134679f"

def get_most_popular(tmdb_key, page):
    return f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_KEY}&sort_by=popularity.desc&page={page}"

def get_by_search(tmdb_key, search_query, page):
    return f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_KEY}&query={search_query}&page={page}"

def get_imdb_id(omdb_key, title):
    return f"http://www.omdbapi.com/?t={title}&apikey={OMDB_KEY}"

def get_by_genre(tmdb_key, page, genre):
    return f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_KEY}&with_genres={genre}&page={page}"

def get_all_genres(tmdb_key):
    return f"https://api.themoviedb.org/3//genre/movie/list?api_key={TMDB_KEY}"


imdb_id = ""
get_movie1 = f"https://gomo.to/movie/{imdb_id}"
get_movie2 = f"https://www.2embed.ru/embed/imdb/movie?id={imdb_id}"

app = Flask(__name__)
app.secret_key = "1234"

@app.route("/")
def root():
	return redirect(url_for("home", page=1))

@app.route("/genre/<genre>/<page>")
def movies_by_genre(genre, page):
    response = get(get_by_genre(TMDB_KEY, page, genre)).text
    data = loads(response)
    response = get(get_all_genres(TMDB_KEY)).text
    all_genres = loads(response)
    return render_template("index.html", content=data["results"], page=int(page), total_pages=data["total_pages"], genres=all_genres["genres"],
    href_prefix=f"/genre/{genre}")

@app.route("/search/<title>/<page>")
def search_movie(page, title):
    # title = request.args["text"]
    response = get(get_by_search(TMDB_KEY, title, page)).text
    data = loads(response)
    
    response = get(get_all_genres(TMDB_KEY)).text
    all_genres = loads(response)
    return render_template("index.html", content=data["results"], page=int(page), total_pages=data["total_pages"], genres=all_genres["genres"],
    href_prefix=f"/search/{title}")

@app.route("/home/<page>", methods=['GET', 'POST'])
def home(page):
    response = get(get_most_popular(TMDB_KEY, page)).text
    data = loads(response)
    response = get(get_all_genres(TMDB_KEY)).text
    all_genres = loads(response)

    print(data['results'])
    return render_template("index.html", content=data["results"], page=int(page), total_pages=500, genres=all_genres["genres"], 
        href_prefix="/home", my_session=session)


@app.route("/movie/<title>")
def get_movie(title):
    response = get(f"http://www.omdbapi.com/?t={title}&apikey=8b7aa942").text
    data = loads(response)
    imdb_id = data["imdbID"]
    # try, exept todo
    # if get(f"https://www.2embed.ru/embed/imdb/movie?id={imdb_id}") != 500:
    # return redirect(f"https://www.2embed.ru/embed/imdb/movie?id={imdb_id}")
    # else:
    return redirect(f"https://gomo.to/movie/{imdb_id}")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        session["user"] = User().signup()
        return home(1)
        

@app.route("/addmovie/<movie>")
def add_movie(movie):
    print(movie)
    User().add_movie(movie)
    
        
@app.route("/favorites")
def favorites():
    
    response = get(get_all_genres(TMDB_KEY)).text
    all_genres = loads(response)
    
    # movies = []
    
    movies = User().get_user(session["user"])
    print(movies)
    return render_template("index.html", content=movies, page=1, total_pages=500, genres=all_genres["genres"], 
        href_prefix="/home", my_session=session)
        

if __name__ == "__main__":
    app.run(debug=True)