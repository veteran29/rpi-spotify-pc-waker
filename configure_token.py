#!/usr/bin/env python3
import sys
import spotipy
import spotipy.util as util
import json

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
    print("Authorized successfully!")
