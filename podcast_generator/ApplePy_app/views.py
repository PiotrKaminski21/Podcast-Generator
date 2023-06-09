from django.shortcuts import render, redirect
from django.views import View

import requests
import random
import re


def get_popular_podcasts():
    url = "https://itunes.apple.com/pl/rss/toppodcasts/limit=100/json"
    response = requests.get(url)
    data = response.json()

    # instrukcja pobierająca 100 najpopularniejszych podcastów z Polski
    if "feed" in data and "entry" in data["feed"]:
        podcasts = []
        for podcast in data["feed"]["entry"]:
            podcast_author = podcast["im:artist"]["label"]
            podcast_name = podcast["im:name"]["label"]
            podcast_image = podcast["im:image"][0]["label"]
            podcast_summary = podcast["summary"]["label"]
            podcast_genre = podcast["category"]["attributes"]["label"]


            # ze względu na długie opisy tutaj ograniczam je do dwóch zdań, wychodzi to nawet nieźle
            summary_sentences = re.split(r'[.!?]',
                                         podcast_summary)  # tutaj program rozpoznaje znaki kończące zdania i zatrzyma się po dwóch takich znakach
            podcast_summary = ' '.join(summary_sentences[:2]) + '.'

            # stworzenie listy podcastów, na której później będzie działać wybór kategorii
            podcasts.append({
                "author": podcast_author,
                "name": podcast_name,
                "image": podcast_image,
                "summary": podcast_summary,
                "genre": podcast_genre,

            })

        return podcasts

    else:
        print("Failed to retrieve podcasts.")
        return []


def get_all_genres():
    url = "https://itunes.apple.com/pl/rss/toppodcasts/limit=100/json"
    response = requests.get(url)
    data = response.json()

    genres = []

    if "feed" in data and "entry" in data["feed"]:
        for podcast in data["feed"]["entry"]:
            podcast_genre = podcast["category"]["attributes"]["label"]
            if podcast_genre not in genres:
                genres.append(podcast_genre)

    else:
        print("Failed to retrieve genres.")

    return genres


# pobiera wszystkie kategorie z 100 najpopularniejszych podcastów w Polsce
all_genres = get_all_genres()

# wyświetlam listę gatunków
for i, genre in enumerate(all_genres):
    print(f"{i + 1}. {genre}")

# tutaj wybieramy w inpucie kategorie, żebyście mogli popróbować
selected_genre_name = input("Choose your favorite genre: ")

if selected_genre_name in all_genres:
    selected_genre = selected_genre_name
    print(f"Your genre: {selected_genre}")

    # tutaj wracam do pierwszej funkcji
    podcasts = get_popular_podcasts()

    # wybiera podcasty z wybranej kategorii
    selected_podcasts = [podcast for podcast in podcasts if podcast["genre"] == selected_genre]

    if len(selected_podcasts) == 0:
        print("No podcasts found in the selected category.")
    else:
        # losowanie trzech podcastów z wybranej kategorii lub wyświetlanie jakichkolwiek dostępnych w tym gatunku
        if len(selected_podcasts) >= 9:
            selected_podcasts = random.sample(selected_podcasts, 9)

        # wybrane podcasty
        for podcast in selected_podcasts:
            print(f"Author: {podcast['author']}")
            print(f"Name: {podcast['name']}")
            print(f"Image: {podcast['image']}")
            print(f"Summary: {podcast['summary']}")

            print("---")

else:
    print("Invalid genre name.")


#klasa strony domowej, prosta bo jedynie renderuje po templatce
class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')


#klasa kategorii konieczna do formularza
class GenreFormView(View):
    def get(self, request):
        all_genres = get_all_genres()
        return render(request, 'form.html', {'genres': all_genres})


    def post(self, request):
        selected_genre_name = request.POST.get('genre')
        all_genres = get_all_genres()

        if selected_genre_name in all_genres:
            selected_genre = selected_genre_name
            podcasts = get_popular_podcasts()
            selected_podcasts = [podcast for podcast in podcasts if podcast["genre"] == selected_genre]

            if len(selected_podcasts) == 0:
                message = "No podcasts found in the selected category."
                return render(request, 'result.html', {'message': message})
            else:
                if len(selected_podcasts) >= 9:
                    selected_podcasts = random.sample(selected_podcasts, 9)

                return render(request, 'result.html', {'podcasts': selected_podcasts})
        else:
            message = "Invalid genre name."
            return render(request, 'result.html', {'message': message})

#tutaj mamy klasę wyników - to wyplute dane + render po templatce
class ResultView(View):
    def get(self, request):
        return redirect('home')
