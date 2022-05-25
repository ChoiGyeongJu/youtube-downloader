from pyparsing import Keyword
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import pytube
from pytube.cli import on_progress
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import pafy
import math
import os, sys


def download_video(urls, saveDir, n):   # n은 다운 받을 비디오 갯수
    for i in range(len(urls)):
        if i == n:
            break
        yt = pytube.YouTube(urls[i], on_progress_callback=on_progress)
        
        yt.streams.filter(progressive=True, file_extension="mp4")\
            .order_by("resolution")\
            .desc()\
            .first()\
            .download(saveDir)

        thumbnails.append(yt.thumbnail_url)
        titles.append(yt.title)


def play_video_by_local(video_dir):  # local 비디오 재생 코드
    cap = cv.VideoCapture(video_dir)

    fps = cap.get(cv.CAP_PROP_FPS)   # 초당 몇프레임인지 
    # frame_count = int(cap.get(cv.CAP_PROP_FRAME_COUNT))    # 프레임 갯수
    # duration = frame_count / fps    # 영상 몇초인지

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            cv.imshow('video', frame)
            if cv.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break    
    cap.release()
    cv.destroyAllWindows() 
    

def play_video_by_url(video_url):  # url 비디오 재생 코드
    video = pafy.new(video_url)
    best  = video.getbestvideo(preftype="any")

    cap = cv.VideoCapture(best.url)

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            cv.imshow('video', frame)
            if cv.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break    
    cap.release()
    cv.destroyAllWindows() 

def capture_image_by_local(video_dir, sec, saveDir):  # local 비디오 캡처 코드
    cap = cv.VideoCapture(video_dir)
    fps = cap.get(cv.CAP_PROP_FPS)

    frame_num = math.floor(fps*sec)    # 30 * 초
    # cap.set(1, frame_num)
    cnt = 0
    while(cap.isOpened()):
        if frame_num > int(cap.get(cv.CAP_PROP_FRAME_COUNT)):
            break
        cap.set(1, frame_num)
        ret, frame = cap.read()

        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        if (ret == True):
            OUTPUT_IMAGE_PATH =  saveDir + '/' + str(KeyWord) + str(cnt) + '.jpg'
            plt.imsave(OUTPUT_IMAGE_PATH, frame)
            frame_num += math.floor(fps*sec)
        else:
            break

        cnt += 1
    cap.release()


def capture_image_by_url(video_url, sec, saveDir, KeyWord):  # url 비디오 캡처 코드
    video = pafy.new(video_url)

    if video.length < sec:    # 영상 길이보다 캡처 지점이 뒤라면,
        sec = video.length

    best  = video.getbestvideo(preftype="any")
    cap   = cv.VideoCapture(best.url)
    fps   = cap.get(cv.CAP_PROP_FPS)

    frame_num = math.floor(fps*sec)    # 30 * 초
    # cap.set(1, frame_num)
    cnt = 0

    print('========캡처중입니다...========')
    while(cap.isOpened()):
        if frame_num > int(cap.get(cv.CAP_PROP_FRAME_COUNT)):
            break
        cap.set(1, frame_num)
        ret, frame = cap.read()

        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        if ret == True:
            OUTPUT_IMAGE_PATH =  saveDir + '/' + str(KeyWord) + str(cnt) + '.jpg'
            plt.imsave(OUTPUT_IMAGE_PATH, frame)
            frame_num += math.floor(fps*sec)
        else:
            break
        cnt += 1
    cap.release()
    print('======캡처가 완료되었습니다======')


def video_download_partially(video_url, saveDir):  # 영상 구간으로 다운하는거, saveDir 경로로 영상 저장됌
    # code = f'youtube-dl --external-downloader ffmpeg --external-downloader-args "-ss 00:01:00 -to 00:01:04"\
    #      -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio" --merge-output-format mp4 {video_url}'  # 화질 좋은 영상 + 소리

    code = f'cd {saveDir} && youtube-dl --external-downloader ffmpeg --external-downloader-args "-ss 00:01:00 -to 00:01:04" -f best {video_url}'   # 화질 안좋은 영상 + 소리

    # code = f'youtube-dl --external-downloader ffmpeg --external-downloader-args "-ss 00:01:00 -to 00:01:04" -f bestvideo {video_url}'   # 소리 X

    os.system(code)



if __name__=='__main__':
    # options = webdriver.ChromeOptions()
    # options.add_experimental_option("excludeSwitches", ["enable-logging"])
    # browser = webdriver.Chrome(ChromeDriverManager().install() ,options=options)

    # KeyWord    = input('검색어를 입력하세요 = ')
    # search_url = "https://www.youtube.com/results?search_query=" + KeyWord

    # image_save_dir = "C:/Users/82102/OneDrive/바탕 화면/" + KeyWord + '/images'

    # os.mkdir("C:/Users/82102/OneDrive/바탕 화면/" + KeyWord)
    # os.mkdir(image_save_dir)

    # browser.get(search_url)
    # browser.maximize_window()

    # soup = bs(browser.page_source, "lxml")

    # video_link_data = browser.find_elements(By.ID,  'video-title')
    
    # url_list       = []
    # titles         = []
    # thumbnails     = []

    # for i in video_link_data:
    #     if i.get_attribute('href') != None:
    #         url_list.append(i.get_attribute('href'))  # urls에 url 목록 저장

    # print(url_list)

    # download_video(url_list,"영상 저장할 경로" , 1)
    
    # play_video_by_local("영상 경로/파일명.mp4")
    # play_video_by_url(url_list[0])

    # capture_image_by_local("영상 경로/파일명.mp4", 40, image_save_dir, KeyWord)
    # capture_image_by_url(url_list[1], 45, image_save_dir, KeyWord)


    url = "영상 youtue url 입력"
    video_download_partially(url, "영상 저장할 경로")