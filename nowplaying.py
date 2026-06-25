import spotipy
import spotipy.util as util

# ===== Input part =====
# creat_playlist = 'test_list_XXX'

# ===== Authentication part =====
# Replace the values below with your own Spotify API credentials.
# Get them at: https://developer.spotify.com/dashboard
username = 'YOUR_SPOTIFY_USERNAME'
my_id = 'YOUR_CLIENT_ID'           # client ID
my_secret = 'YOUR_CLIENT_SECRET'   # client secret
redirect_uri = 'http://localhost:8888/callback'

# Scopes used to grant permissions to the app
scope = 'user-library-read user-read-playback-state playlist-read-private user-read-recently-played playlist-read-collaborative playlist-modify-public playlist-modify-private'

token = util.prompt_for_user_token(username, scope, my_id, my_secret, redirect_uri)
spotify = spotipy.Spotify(auth=token)

# spotify.user_playlist_create(user=username, name=creat_playlist)

current_track = spotify.current_user_playing_track()

if current_track is None:
    text = 0
else:
    artistname = current_track['item']['artists'][0]['name']
    titlename = current_track['item']['name']

    # print(current_track)
    text = artistname + " - " + titlename

print(text)
