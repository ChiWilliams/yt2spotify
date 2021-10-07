from urllib.parse import unquote

import spotipy
from flask import Flask, request, Response
from spotipy.oauth2 import SpotifyClientCredentials

from yt2spotify.converter import Converter
from yt2spotify.services.spotify import SpotifyService, read_spotify_config
from yt2spotify.services.youtube_music import YoutubeMusicService

application = Flask(__name__)

client_id, client_secret = read_spotify_config('config.ini')
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

youtube_to_spotify = Converter(YoutubeMusicService(), SpotifyService(sp))


@application.route('/')
def index():
    return application.send_static_file('index.html')


@application.route('/y2s')
def yt2spotify():
    url = request.args.get('url')
    if url == "" or url is None:
        return Response("no URL parameter in request", status=400)

    url = unquote(url)
    try:
        result = youtube_to_spotify.convert(url)
        return Response(response=result.json(), status=200, mimetype='application/json')
    except ValueError as e:
        return Response(response=str(e), status=400)
    except Exception as e:
        return Response(response="That didn't work.", status=500)


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000)
