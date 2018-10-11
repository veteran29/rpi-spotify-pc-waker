#!/usr/bin/env python3

import sys
import spotipy
import spotipy.util as util
import json
from time import sleep

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
	
	# Some time for spotify client to initialize
	sleep(15)
	print("Starting playback...")

	try:
		play_on_target(config["target-player"], config["target-music"], True, 30)
	except:
		print("Error while trying to play music")
		print("Wait 15s and try again")
		sleep(15)
		# Try again
		try:
			play_on_target(config["target-player"], config["target-music"], True, 30)
		except:
			print("Playback failed ;-(\nExiting.")
			exit()

		playing_info = sp.current_user_playing_track()
		print("Track: %s" % playing_info["item"]["name"])


	else:
		print("Can't get token for", config["username"])
