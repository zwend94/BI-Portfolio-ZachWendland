import requests
import pandas as pd

#API Credentials
CLIENT_ID = "01610abcafbc4bc6899f1217cd4407a9"
CLIENT_SECRET = "0ad83c8b2e3642b38a7ad2aaa58ab3ed"

#Genres
GENRES = ["alternative", "punk-rock", "pop-punk", "emo", "metalcore", "pop-rock", "metal"]

#Token
def get_spotify_token(client_id, client_secret):
    url = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, headers=headers, data=data, auth=(client_id, client_secret))
    return response.json().get("access_token")

#Top Artists by Genre
def fetch_top_artists_by_genre(genre, token, limit=50):
    url = f"https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "q": f"genre:{genre}",
        "type": "artist",
        "limit": limit
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json().get("artists", {}).get("items", [])

import os 

os.chdir('C:/Users/lyyud/Documents/spotify_project')
#Main Script
def main():
    token = get_spotify_token(CLIENT_ID, CLIENT_SECRET)
    all_artists = []

    for genre in GENRES:
        print(f"Fetching top artists for genre: {genre}")
        artists = fetch_top_artists_by_genre(genre, token, limit=50)
        for artist in artists:
            followers = artist.get("followers", {}).get("total", 0)
            popularity = artist.get("popularity", 0)
            genres = artist.get("genres", [])
            followers_to_popularity = round((followers / popularity) * 100, 2) if popularity > 0 else 0
            num_genres = len(genres)

            years_active = "Unknown"

            all_artists.append({
                "Artist Name": artist.get("name"),
                "Genre": genre,
                "Popularity": popularity,
                "Followers": followers,
                "ID": artist.get("id"),
                "URI": artist.get("uri"),
                "Followers to Popularity (%)": followers_to_popularity,
                "Number of Genres": num_genres,
                "Genres": ", ".join(genres),
                "Years Active": years_active
            })

    #Save to CSV
    df = pd.DataFrame(all_artists)
    df.to_csv("top_artists_by_genre.csv", index=False)
    print("Data saved to top_artists_by_genre.csv")

if __name__ == "__main__":
    main()

import pandas as pd

df = pd.read_csv('top_artists_by_genre.csv')

print(df)
