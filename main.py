# SPOTIFY PLAYLIST CREATOR

from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# U can get them by signing in spotify for developers
SPOTIPY_CLIENT_ID = "1c0b5864e26d48d7b972e1be43b8ad9d"
SPOTIPY_CLIENT_SECRET = "a18d5a0e80b14ba4b31ecb8d3997e58e"
SPOTIPY_REDIRECT_URI = "http://example.com"
# Getting inputs
date = input("What year do you want to travel YYYY-MM-DD? ")
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
web_data = response.text
# Bs4 and authentication
soup = BeautifulSoup(web_data, "html.parser")
titles_tag = soup.select("li ul li h3")
title = [name.string.strip() for name in titles_tag]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username="Billboard of Spotify"
    )
)
user_id = sp.current_user()["id"]
# Isolating the song url and adding to a playlist
songs_uri = []
year = date.split("-")[0]
for song in title:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        songs_uri.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist_id = sp.user_playlist_create(user_id, f"{date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist_id["id"], items=songs_uri)
