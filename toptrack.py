import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify artist URI to look up top tracks for.
# Example below is a placeholder artist URI.
lz_uri = 'spotify:artist:XXXXXXXXXXXXXXXXXXXXXX'

# Replace the values below with your own Spotify API credentials.
# Get them at: https://developer.spotify.com/dashboard
my_id = 'YOUR_CLIENT_ID'           # client ID
my_secret = 'YOUR_CLIENT_SECRET'   # client secret

ccm = SpotifyClientCredentials(client_id=my_id, client_secret=my_secret)
spotify = spotipy.Spotify(client_credentials_manager=ccm)
results = spotify.artist_top_tracks(lz_uri)

for track in results['tracks'][:10]:
    print('track    : ' + track['name'])
    print('audio    : ' + str(track['preview_url']))
    print('cover art: ' + track['album']['images'][0]['url'])
    print()
