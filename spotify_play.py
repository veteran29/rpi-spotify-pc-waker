import sys
import spotipy
import spotipy.util as util
import json

global sp

def play_on_target(target, uri, shuffle = False, volume = 15):
    """Play uri on target device"""
    sp.shuffle(shuffle, target)
    sp.volume(volume, target)
    sp.start_playback(target, uri)

def play_music():

    with open('settings.json') as f:
        config = json.load(f)["spotify"]

    token = util.prompt_for_user_token(
        config["username"],
        config["scopes"],
        config["client-id"],
        config["client-secret"],
        config["redirect-uri"]
    )

    if token:
        global sp
        sp = spotipy.Spotify(auth=token)
        playlists = sp.current_user_playlists()

        print("starting playback...")

        play_on_target(config["target-player"], "spotify:playlist:148My4xA7WoEaNDmnl2A8Z", True, 30)

        playing_info = sp.current_user_playing_track()
        print("Track: %s" % playing_info["item"]["name"])


    else:
        print("Can't get token for", config["username"])
