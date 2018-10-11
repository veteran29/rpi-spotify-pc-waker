#!/usr/bin/env python3

import subprocess
import datetime
import json
from time import sleep
from wakeonlan import send_magic_packet
# Local module which will start the music on target PC
import spotify_play

with open('settings.json') as f:
        config = json.load(f)["checker"]

start_time = datetime.time(16,30)
end_time = datetime.time(19,25)

def should_run():
	"""Checks time is between specified hours"""
	current_time = datetime.datetime.now().time()

	return (current_time > start_time) and (current_time < end_time)

def is_device_up(host):
	"""Checks if given host is up via ping"""
	ping_result = subprocess.call(
			"ping -c 5 -n -W 4 " + host + " >/dev/null",
			shell=True
		)

	return ping_result == 0

def wait_for_pc():
	wait_seconds = 240
	interval = 15
	while wait_seconds > 0:
		if is_device_up(config["spotify-host"]):
			print("Spotify host is up, playing music.")
			spotify_play.play_music()

			return True

		sleep(interval)
		wait_seconds -= interval

	print("Time is up...")
	return False


try:
	print(datetime.datetime.now().time())
	while True:
		if should_run() == False:
			print("Current time out of execution range, stopping.")
			print(datetime.datetime.now().time())
			exit()


		if is_device_up(config["trigger-host"]):
			print("phone is connected")
			print(datetime.datetime.now().time())
			print("Waking up pc")
			send_magic_packet(config["spotify-host-mac"])
			wait_for_pc()

			exit()

		sleep(30)

except KeyboardInterrupt:
	exit()

