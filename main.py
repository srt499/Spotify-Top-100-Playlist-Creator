import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Get top 100 songs for a given date from Billboard website
date = input("What year-month-day would you like the top 100 songs from? ")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
contents = response.text

soup = BeautifulSoup(contents, "html.parser")

song_tags = soup.select(".a-no-trucate")
artist_tags = soup.find_all(name="span", class_="a-font-primary-s")
song_titles = [song.getText().strip() for i, song in enumerate(song_tags) if i % 2 == 0]
artists = [artist.getText().strip() for artist in artist_tags]
for artist in artists:
    if artist == "RIAA Certification:":
        artists.remove(artist)


# Setup Spotify API using Spotipy library/module and use it to search for and create a new playlist comprised of top
# 100 songs from Billboard
cid = "!! Get From Spotify !!"
secret = "!! Get From Spotify !!"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=cid,
        client_secret=secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]

# Searching Spotify for songs by title

# song_uris = [sp.search(title)['tracks']['items'][0]['uri'] for title in song_titles]
song_uris = []
for i, title in enumerate(song_titles):
    results = sp.search(q=f"track={title} artist={artists[i]}", type="track")
    try:
        song_uris.append(results["tracks"]["items"][0]["uri"])
    except:
        pass
# print(song_uris)
# print(len(song_uris))

# Create a spotify playlist using Spotipy library
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

# Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
