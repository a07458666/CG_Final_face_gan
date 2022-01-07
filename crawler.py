# -*- coding: utf-8 -*- 
import os
import time
import math
import datetime
import argparse
import pandas as pd
from pytube import YouTube
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
import ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context


def scroll_page(pages):
    for i in range(1, pages):
        height = i * 10000
        chrome.execute_script(f'window.scrollTo(0,{height})')
        time.sleep(10)


def get_playlist_videos(playlist_url):
    chrome.get(playlist_url)
    time.sleep(3)
    list_page = BeautifulSoup(chrome.page_source, 'html.parser')
    # Compute number of pages to scroll
    if args.update:
        pages = 1
    else:
        video_num = list_page.find('div',{'id':'stats','class':'style-scope ytd-playlist-sidebar-primary-info-renderer'}).find('span').get_text()
        video_num = int(video_num.replace(',', ''))
        pages = math.ceil(video_num / 100) + 1
        scroll_page(pages)

    # Get video list from playlist page
    list_page = BeautifulSoup(chrome.page_source, 'html.parser')
    video_list = list_page.find_all('ytd-playlist-video-renderer',class_='style-scope ytd-playlist-video-list-renderer')
    get_videos_info(video_list, "")


def get_videos_info(video_list, key_word):

    # Process every video
    for i, v in enumerate(video_list):
        try:
            # Get video id
            href = v.find('a').get('href')
            video_id = href.split('&')[0]
            id = video_id.split('=')[1]
        except:
            print(f'Index: {i}  Can not parse video id: {href}')
            continue
        try:
            print(video_url_base + id)
            # Get vedio page
            video = YouTube(video_url_base + id)
        except:
            print(f'Index: {i}  Can not get YouTube page: {id}')
            continue
        chrome.get(video_url_base + id)
        time.sleep(5)
        video_page = BeautifulSoup(chrome.page_source, 'html.parser')
        
        if video.length <= 360:
            # Get video information
            author = video.author
            title = video.title
            description = video.description
            length = video.length
            try:
                date_str = video_page.find('div', {'id' :'info-strings','class':'style-scope ytd-video-primary-info-renderer'}).find('yt-formatted-string').get_text()
            except:
                print(f'Index: {i}  Can not get date string: {id}')
                continue
            if date_str.find('預定') != -1 or date_str.find('Scheduled') != -1:
                print(f'Index: {i}  is scheduled video')
                continue
            if date_str.find('開始直播時間') != -1 or date_str.find('Started streaming') != -1:
                print(f'Index: {i}  is streaming video')
                continue
            try:
                date_obj = datetime.datetime.strptime(date_str, '%Y年%m月%d日')
            except:
                try: 
                    date_obj = datetime.datetime.strptime(date_str, '%b %d, %Y')
                except: 
                    try:
                        date_obj = datetime.datetime.strptime(date_str, '首播日期：%Y年%m月%d日')
                    except:
                        date_obj = datetime.datetime.strptime(date_str, 'Premiered %b %d, %Y')
            
            upload_date = date_obj.strftime('%Y-%m-%d')
                
            hashtag_list = video_page.find_all('a',class_='yt-simple-endpoint style-scope yt-formatted-string')
            hashtags = []
            for h in hashtag_list:
                tag = h.get_text()
                if '#' in tag and tag not in hashtags:
                    tag = tag[1:]
                    hashtags.append(tag)
            hashtags = str(hashtags)
        
            # Set file path and save video
            file_path = f'{data_path}/data/video/{upload_date}'
            if not os.path.exists(file_path):
                Path(file_path).mkdir(parents=True, exist_ok=True)
            video.streams.filter(subtype='mp4').first().download(file_path,filename=f'{id}.mp4')

        else:
            print(f'Index: {i}  Video length is over 6 minutes: {id}')


data_path = "static"
video_url_base = 'https://www.youtube.com/watch?v='
query_url_base = 'https://www.youtube.com/results?search_query='

# Get command line parameter
parser = argparse.ArgumentParser()
g_search = parser.add_argument_group('Search mode', 'Parameter for search mode')
g_search.add_argument('-k', '--keyword', type=str, help='Keyword for searching')
g_search.add_argument('-f', '--filter', type=str, help='Searching filter', default='w', choices=['a', 'y', 'm', 'w', 'd', 's'])
g_playlist = parser.add_argument_group('Playlist mode', 'Parameter for playlist mode')
g_playlist.add_argument('-p', '--playlist', type=str, help='Crawl from given playlist url')
g_playlist.add_argument('-u', '--update', help='Crawl from existed playlist', action='store_true')
args = parser.parse_args()

# Set web driver
options = Options()
options.add_argument("--disable-notifications")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1420,1080')
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
s=Service(ChromeDriverManager().install())
chrome = webdriver.Chrome(service=s, options=options)


# list_df = pd.read_csv('playlist.csv',encoding='utf8')
# playlist_url_list = list_df['list_url'].tolist()

if args.playlist:
    # Write new playlist infomation
    if args.playlist not in list_df['list_url'].values:
        chrome.get(args.playlist)
        time.sleep(3)
        list_page = BeautifulSoup(chrome.page_source, 'html.parser')
        list_name = list_page.find('h1',id='title').get_text()
        author = list_page.find('div',{'id':'text-container','class':'style-scope ytd-channel-name'}).find('a').get_text()
        list_df = list_df.append({
                    "list_url":args.playlist,
                    "list_name":list_name,
                    "author":author
                    }, ignore_index=True)
        list_df.to_csv('playlist.csv', encoding='utf8', index=False)
    get_playlist_videos(args.playlist)

if args.update:
    for url in playlist_url_list:
        get_playlist_videos(url)

if args.keyword:
    key_word = args.keyword
    if args.filter == 'a':
        # 影片、短片、以上傳日期排序
        sp = 'CAISBhABGAEgAQ%253D%253D'  #'CAISBBABGAE%253D'  #'EgQQARgB' #'CAISAhgB'
        pages = 500  #100
    elif args.filter == 'y':
        # 今年、影片、短片、以上傳日期排序
        sp = 'CAISBggFEAEYAQ%253D%253D'
        pages = 50
    elif args.filter == 'm':
        # 本月、影片、短片、以上傳日期排序
        sp = 'CAISBggEEAEYAQ%253D%253D'
        pages = 20
    elif args.filter == 'w':
        # 本週、影片、短片、以上傳日期排序
        sp = 'CAISBggDEAEYAQ%253D%253D'
        pages = 10
    elif args.filter == 's':
        # sp
        sp = 'EgIQAQ%253D%253D'
        pages = 100
    else:
        # 今天、影片、短片、以上傳日期排序
        sp = 'CAISBggCEAEYAQ%253D%253D'
        pages = 5

    chrome.get(query_url_base + key_word + '&sp=' + sp)
    scroll_page(pages)
    
    # Get video list from search result page
    list_page = BeautifulSoup(chrome.page_source, 'html.parser')
    video_list = list_page.find('div',{'id':'contents','class':'style-scope ytd-section-list-renderer'}).find_all('ytd-video-renderer', class_='style-scope ytd-item-section-renderer')
    get_videos_info(video_list, key_word)
    
chrome.quit() 