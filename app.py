from flask import Flask, request, render_template, redirect, url_for
import requests
import urllib.parse

app = Flask(__name__)

CLIENT_ID = 'f07166fe99d94f649205f91c96448061'
CLIENT_SECRET = 'ef8fb745abda4f179276e26a780bb557'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    try:
        query = request.args.get('q')
        region = 'US'
        tracks, unique_artists = [], {}
        num_artists = 10
        num_tracks = 50
        forbidden_chars = "ЁёЪъЫыЭэ"  # No spaces in the set

        if query:
            access_token = get_access_token()
            if access_token:
                headers = {'Authorization': f'Bearer {access_token}'}
                # Fetch Tracks
                track_params = {'q': query, 'type': 'track', 'limit': num_tracks, 'market': region}
                track_response = requests.get('https://api.spotify.com/v1/search', headers=headers, params=track_params)
                if track_response.status_code == 200:
                    track_json = track_response.json()
                    track_items = track_json.get('tracks', {}).get('items', [])
                    for track in track_items:
                        if track['preview_url'] and not any(ch in forbidden_chars for ch in track['name']) and len(tracks) < 10:
                            tracks.append(track)

                # Fetch Artists
                artist_params = {'q': query, 'type': 'artist', 'limit': num_artists}
                artist_response = requests.get('https://api.spotify.com/v1/search', headers=headers, params=artist_params)
                if artist_response.status_code == 200:
                    artist_json = artist_response.json()
                    artist_items = artist_json.get('artists', {}).get('items', [])
                    for artist in artist_items:
                        if artist['id'] not in unique_artists and not any(ch in forbidden_chars for ch in artist['name']):
                            unique_artists[artist['id']] = artist
                            unique_artists[artist['id']]['image_url'] = artist['images'][0]['url'] if artist['images'] else "default.jpg"

        return render_template('results.html', search_query=query, tracks=tracks, artists=list(unique_artists.values()))
    except Exception as e:
        print(repr(e))
        return render_template('error.html', error_message=str(e))





@app.route('/similar/<song_id>/<song_name>')
def similar_songs(song_id, song_name):
    access_token = get_access_token()
    if not access_token:
        return redirect(url_for('index'))

    headers = {'Authorization': f'Bearer {access_token}'}
    params = {
        'seed_tracks': song_id,
        'limit': 50,
        'market': 'US'
    }
    forbidden_chars = "ЁёЪъЫыЭэ"  # No spaces in the set
    try:
        response = requests.get(f'https://api.spotify.com/v1/recommendations', headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            tracks = [track for track in data.get('tracks', []) if track['preview_url'] and not any(ch in forbidden_chars for ch in track['name'])]
            filtered_tracks = tracks[:10]

            if not filtered_tracks:
                return render_template('no_data.html', song_name=urllib.parse.unquote(song_name))
            song_name_decoded = urllib.parse.unquote(song_name)
            return render_template('similar.html', tracks=filtered_tracks, song_name=song_name_decoded)
        else:
            print(f"Spotify API Error: HTTP {response.status_code} - {response.text}")
            return render_template('error.html', error_message="Failed to fetch similar tracks.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return render_template('error.html', error_message=str(e))









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



