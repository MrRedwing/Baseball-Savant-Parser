from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from download import clear_folder, get_url, download_video_series

import time
import os

import requests 

import json
import pandas as pd

def savant_site_static(url, batter=True, sort_type='basic'):
    # clearing data folder
    clear_folder('data')

        # Start chrome browser and retrieve web page
    chrome_options = Options()
    # chrome_options.add_argument("--headless")

    download_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    prefs = {"download.default_directory":download_location}
    chrome_options.add_experimental_option("prefs", prefs)

    browser = webdriver.Chrome(options=chrome_options)
    browser.get(url)

    # downloading data
    csv_download = browser.find_elements(By.XPATH, '//*[@id="csv_all_pid_"]/img')
    # print(csv_download)

    csv_download[0].click()

    # quiting slow webdriver
    time.sleep(1)
    browser.quit()

    file_name = os.path.join(download_location, 'savant_data.csv')
    csv_data = pd.read_csv(file_name)

    if sort_type == 'recent':
    # Sort by most recent
        recent = csv_data.sort_values(by=["game_date"], ascending=False)
        csv_data = recent
    elif sort_type == 'latest':
    # Sort by first
        latest = csv_data.sort_values(by=["game_date"], ascending=True)
        csv_data = latest
    
    clips = []
    length = len(csv_data)
    for index, row in csv_data.iterrows():
        # print(index, row)
        clips.append(savant_clip(row, batter))
        print(f'{index} / {length}', end="\r")

    # possible sorting added for different situation
    # sort by player and order of event
    # sort by order of event
    clear_folder('videos')
    download_video_series('videos', clips)

def iterate(array, key, value):
    new_array = []
    for item in array:
        if str(item[key]) == str(value):
            new_array.append(item)
    
    return new_array

def savant_clip(pitch, batter):
    # find row needed and provide game_pk and other info
    game_url = "https://baseballsavant.mlb.com/gf?game_pk="+str(pitch["game_pk"])
    # print(game_url)
    game = requests.get(game_url)
    
    game_json = json.loads(game.text)

    if batter:
        if pitch["inning_topbot"] == "Top":
            team = game_json["team_home"]
            broadcast_type = "&videoType=AWAY"
        else:
            team = game_json["team_away"]
            broadcast_type = "&videoType=HOME"
    else:
        if pitch["inning_topbot"] == "Top":
            team = game_json["team_away"]
            broadcast_type = "&videoType=HOME"
        else:
            team = game_json["team_home"]
            broadcast_type = "&videoType=AWAY"

    team = iterate(team, "ab_number", pitch["at_bat_number"])
    team = iterate(team, "pitch_number", pitch["pitch_number"])

    site_url = "https://baseballsavant.mlb.com/sporty-videos?playId="+team[0]["play_id"]+broadcast_type
    clip_url = get_url(site_url)

    # print(site_url)

    if clip_url != "":
        return clip_url
    
    site_url = "https://baseballsavant.mlb.com/sporty-videos?playId="+team[0]["play_id"]+"&videoType=NETWORK"
    clip_url = get_url(site_url)

    return clip_url

