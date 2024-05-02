from flask import Flask, request, render_template
import requests

app = Flask(__name__)

CLIENT_ID = 'f07166fe99d94f649205f91c96448061'
CLIENT_SECRET = 'ef8fb745abda4f179276e26a780bb557'

@app.route('/')
def index():
    return render_template('index.html')

def get_songs_for_artist(artist_id, access_token):
    try:
        headers = {'Authorization': f'Bearer {access_token}'}
        tracks_response = requests.get(f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US', headers=headers)
        if tracks_response.status_code == 200:
            tracks_data = tracks_response.json().get('tracks', [])[:3]  # Limit to 3 songs
            #print(f"Tracks for Artist ID {artist_id}: {tracks_data}")  # Debug print
            return tracks_data
        else:
            print(f"Failed to retrieve tracks for artist {artist_id}: {tracks_response.status_code}")
            return []
    except Exception as e:
        print(f"Exception while getting songs for artist {artist_id}: {str(e)}")
        return []


@app.route('/search')
def search():
    try:
        query = request.args.get('q')
        tracks, unique_artists = None, {}
        if query:
            access_token = get_access_token()
            if access_token:
                headers = {'Authorization': f'Bearer {access_token}'}
                search_params = {'q': query, 'type': 'track,artist', 'limit': 10}
                response = requests.get('https://api.spotify.com/v1/search', headers=headers, params=search_params)
                if response.status_code == 200:
                    json_response = response.json()
                    tracks = json_response.get('tracks', {}).get('items', [])
                    artist_items = json_response.get('artists', {}).get('items', [])
                    for artist in artist_items:
                        if artist['id'] not in unique_artists:
                            artist_songs = get_songs_for_artist(artist['id'], access_token)
                            unique_artists[artist['id']] = artist
                            unique_artists[artist['id']]['songs'] = artist_songs
                            unique_artists[artist['id']]['image_url'] = artist['images'][0]['url'] if artist['images'] else "patron.jpg"
        return render_template('results.html', search_query=query, tracks=tracks, artists=list(unique_artists.values()))
    except Exception as e:
        print(e)  # For debug, use logging in production
        return render_template('error.html')  # A generic error page


def get_access_token():
    token_url = 'https://accounts.spotify.com/api/token'
    data = {'grant_type': 'client_credentials'}
    auth = (CLIENT_ID, CLIENT_SECRET)
    response = requests.post(token_url, data=data, auth=auth)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        print("Failed to retrieve access token:", response.status_code, response.text)
        return None


if __name__ == '__main__':
    app.run(debug=True)














































@app.route('/top-ukrainian-songs')
def top_ukrainian_songs():
    access_token = get_access_token()
    tracks = []
    if access_token:
        genre = request.args.get('genre', '')  # Handle the case where genre might not be provided
        headers = {'Authorization': f'Bearer {access_token}'}
        params = {'q': f'genre:"ukrainian {genre}"', 'type': 'track', 'limit': 10}
        response = requests.get('https://api.spotify.com/v1/search', headers=headers, params=params)
        if response.status_code == 200:
            tracks = response.json().get('tracks', {}).get('items', [])
    return render_template('top_ukrainian_songs.html', tracks=tracks)

@app.route('/ukrainian-genres')
def ukrainian_genres():
    access_token = get_access_token()
    ukrainian_genres = []
    if access_token:
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get('https://api.spotify.com/v1/recommendations/available-genre-seeds', headers=headers)
        if response.status_code == 200:
            genres = response.json().get('genres', [])
            ukrainian_genres = [f"ukrainian {genre}" for genre in genres if "ukrainian" in genre or genre in ['pop', 'rock', 'dance']]
    return render_template('ukrainian_genres.html', genres=ukrainian_genres)



