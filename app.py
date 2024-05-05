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
        max_results = 10  # Maximum results for both tracks and artists
        forbidden_chars = "ЁёЪъЫыЭэ"  # No spaces in the set

        if query:
            access_token = get_access_token()
            if access_token:
                headers = {'Authorization': f'Bearer {access_token}'}
                tracks, unique_artists = {}, {}

                # Fetch Tracks
                track_params = {'q': query, 'type': 'track', 'limit': max_results}
                track_response = requests.get('https://api.spotify.com/v1/search', headers=headers, params=track_params)
                if track_response.status_code == 200:
                    track_json = track_response.json()
                    track_items = track_json.get('tracks', {}).get('items', [])
                    for track in track_items:
                        if not any(ch in forbidden_chars for ch in track['name']):
                            tracks[track['id']] = track  # Store track by id for easy access

                # Fetch Artists
                artist_params = {'q': query, 'type': 'artist', 'limit': max_results}
                artist_response = requests.get('https://api.spotify.com/v1/search', headers=headers, params=artist_params)
                if artist_response.status_code == 200:
                    artist_json = artist_response.json()
                    artist_items = artist_json.get('artists', {}).get('items', [])
                    for artist in artist_items:
                        if artist['id'] not in unique_artists and not any(ch in forbidden_chars for ch in artist['name']):
                            # Store only up to 3 genres per artist
                            artist['genres'] = artist.get('genres', [])[:3]
                            artist['image_url'] = artist['images'][0]['url'] if artist['images'] else "default.jpg"
                            unique_artists[artist['id']] = artist
                            if len(unique_artists) >= max_results:
                                break  # Stop adding artists if we reach the max results

                # Attach genres to tracks
                for track_id, track in tracks.items():
                    # Assume the first artist is representative for genre information
                    first_artist_id = track['artists'][0]['id']
                    track['artist_genres'] = unique_artists[first_artist_id]['genres'] if first_artist_id in unique_artists else []

                        # Check if both tracks and artists are empty
                if not tracks and not unique_artists or not query:
                  return render_template('no_data.html', search_query=query)
        elif not query:
          return render_template('no_data.html', search_query=query)
        return render_template('results.html', search_query=query, tracks=list(tracks.values()), artists=list(unique_artists.values()))
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
        'limit': 15,
        'market': 'US'
    }
    forbidden_chars = "ЁёЪъЫыЭэ"  # No spaces in the set
    try:
        response = requests.get(f'https://api.spotify.com/v1/recommendations', headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            tracks = data.get('tracks', [])
            enhanced_tracks = []

            for track in tracks:
                if track['preview_url'] and not any(ch in forbidden_chars for ch in track['name']):
                    # Fetch each artist's genres for the track
                    if track['artists']:
                        artist_id = track['artists'][0]['id']
                        artist_response = requests.get(f'https://api.spotify.com/v1/artists/{artist_id}', headers=headers)
                        if artist_response.status_code == 200:
                            artist_data = artist_response.json()
                            genres = artist_data.get('genres', [])[:3]  # Limit to 3 genres
                            track['artist_genres'] = genres
                        else:
                            track['artist_genres'] = []
                    enhanced_tracks.append(track)

            filtered_tracks = enhanced_tracks[:9]

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




@app.route('/similar_artist/<artist_id>/<artist_name>')
def similar_artists(artist_id, artist_name):
    access_token = get_access_token()
    if not access_token:
        return redirect(url_for('index'))

    headers = {'Authorization': f'Bearer {access_token}'}
    url_related_artists = f'https://api.spotify.com/v1/artists/{artist_id}/related-artists'
    forbidden_chars = "ЁёЪъЫыЭэ"

    try:
        response_related = requests.get(url_related_artists, headers=headers)
        if response_related.status_code == 200:
            data_related = response_related.json()
            artists = data_related.get('artists', [])

            # Fetch top tracks and genres for each artist
            for artist in artists:
                # Get top tracks
                url_top_tracks = f'https://api.spotify.com/v1/artists/{artist["id"]}/top-tracks?market=US'
                response_tracks = requests.get(url_top_tracks, headers=headers)
                tracks_data = response_tracks.json() if response_tracks.status_code == 200 else {'tracks': []}
                artist['top_tracks'] = tracks_data.get('tracks', [])[:2]

                # Fetch genres from artist details, already available in the initial fetch
                artist['genres'] = ', '.join(artist['genres'][:3])

            filtered_artists = [artist for artist in artists if not any(ch in forbidden_chars for ch in artist['name'])][:9]

            if not filtered_artists:
                return render_template('no_data.html', artist_name=urllib.parse.unquote(artist_name))
            artist_name_decoded = urllib.parse.unquote(artist_name)
            return render_template('similar_artists.html', artists=filtered_artists, artist_name=artist_name_decoded)
        else:
            print(f"Spotify API Error: HTTP {response_related.status_code} - {response_related.text}")
            return render_template('error.html', error_message="Failed to fetch similar artists.")
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



