import os
import requests
from tqdm import tqdm

from bs4 import BeautifulSoup

def clear_folder(path):
    # deletes current files in folder
    mypath = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
    for f in os.listdir(mypath):
            os.unlink(os.path.join(mypath, f))

def get_url(site_url):
    site = requests.get(site_url)

    soup = BeautifulSoup(site.text, features="html.parser")
    video_obj = soup.find("video", id="sporty")
    clip_url = video_obj.find('source').get('src')

    return clip_url

def download_video_series(path, video_links): 
    #downloads video links to mp4s in folder
    for i, link in tqdm(enumerate(video_links)): 
        # numbers off homerun numberings
        file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), path, f'clip_{i}.mp4')

        for z in range(5):
            try:
                r = requests.get(link, stream = True, timeout=60) 
                break
            except Timeout:
                print(f'Timeout has been raised. Link: {link}')

        # download started 
        with open(file_name, 'wb') as f: 
            for chunk in r.iter_content(chunk_size = 1024*1024): 
                if chunk: 
                    f.write(chunk) 

        # print(f"{file_name} downloaded!")

    print("All videos downloaded!")
    return

def download_video(path, link, number):
    file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), path, f'clip_{number}.mp4')

    for z in range(5):
        try:
            r = requests.get(link, stream = True, timeout=15) 
            break
        except Timeout:
            print(f'Timeout has been raised. Link: {link}')

    # download started 
    with open(file_name, 'wb') as f: 
        for chunk in r.iter_content(chunk_size = 1024*1024): 
            if chunk: 
                f.write(chunk) 

    print(f'{file_name} download!')

    return

def validate(text, comp1='y', comp2='n'):
    answer = input(text).strip().lower()

    while answer != comp1 and answer != comp2:
        print('Invalid response: ')
        answer = input(text).strip().lower()

    if answer == comp1:
        return True
    return False
