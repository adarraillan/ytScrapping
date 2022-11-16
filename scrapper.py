# -*- coding: utf-8 -*-
import json

import requests, re
import time
import sys, getopt

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

tryWithTheComments = True

def getTheRequestedUrl(video_id : str)-> requests.models.Response:
    return requests.get("https://www.youtube.com/watch?v=" + video_id)


def transformTheVideoIntoSoup(video_id : str)-> BeautifulSoup:
    request = getTheRequestedUrl(video_id)
    return BeautifulSoup(request.text, "html.parser")

def getTheVideoTitle(soup : BeautifulSoup)-> str:
    return soup.select_one('meta[itemprop="name"][content]')['content']

def getTheVideoViews(soup : BeautifulSoup)-> str:
    return soup.select_one('meta[itemprop="interactionCount"][content]')['content']

def getTheVideoId(soup : BeautifulSoup)-> str:
    return soup.select_one('meta[itemprop="videoId"][content]')['content']

def getTheVideoDescription(soup : BeautifulSoup)-> str:
    pattern = re.compile('(?<=shortDescription":").*(?=","isCrawlable)')
    return pattern.findall(str(soup))[0].replace('\\n', '\n')

def getTheVideoChannelName(soup : BeautifulSoup)-> str:
    return soup.select_one('link[itemprop="name"][content]')['content']

def getTheVideoNumberOfLikes(soup : BeautifulSoup)-> str:
    data = re.search(r"var ytInitialData = ({.*?});", soup.prettify()).group(1)
    data_json = json.loads(data)
    try:
        likesString = data_json['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0][
            'videoPrimaryInfoRenderer']['videoActions']['menuRenderer']['topLevelButtons'][0][
            'segmentedLikeDislikeButtonRenderer']['likeButton']['toggleButtonRenderer']['defaultText']['accessibility'][
            'accessibilityData']['label']
        numberOfLikes = "".join([i for i in likesString if i.isdigit()])
    except:
        numberOfLikes = '0'

    return numberOfLikes

def getTheExternalLinksWithinVideoDescription(soup : BeautifulSoup)-> list:
    return re.findall(r'(https?://\S+)', getTheVideoDescription(soup))

def getTheVideoComments(video_id : str)-> list:
    services = Service(ChromeDriverManager().install())
    options = Options()

    driver = webdriver.Chrome(service=services, options=options)
    driver.get("https://www.youtube.com/watch?v=" + video_id)
    time.sleep(2)

    allTheComments = []
    element = driver.find_element(By.XPATH, "//*[@id=\"comments\"]")
    driver.execute_script("arguments[0].scrollIntoView();", element)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    commentsList = soup.find_all("ytd-comment-thread-renderer", {"class": "style-scope ytd-item-section-renderer"}, limit = 5)
    timer = 0
    while commentsList == []:
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        commentsList = soup.find_all("ytd-comment-thread-renderer", {"class": "style-scope ytd-item-section-renderer"}, limit = 5)
        timer += 1
        if timer == 3:
            print('--',getTheVideoTitle(soup), '-- takes to much time to load the comments, maybe there is no comments')
            break

    for comment in commentsList:
        allTheComments.append(comment.find("yt-formatted-string", {"id": "content-text"}).text)

    return allTheComments

def createADictionnaryWithAllTheInformations(video_id : str)-> dict:
    if tryWithTheComments:
        comments = getTheVideoComments(video_id)
    else:
        comments = []

    soup = transformTheVideoIntoSoup(video_id)
    return {
        soup.find("meta", itemprop="videoId")["content"]: {
            "title": getTheVideoTitle(soup),
            "views": getTheVideoViews(soup),
            "channelName": getTheVideoChannelName(soup),
            "description": getTheVideoDescription(soup),
            "numberOfLikes": getTheVideoNumberOfLikes(soup),
            "externalLinks": getTheExternalLinksWithinVideoDescription(soup),
            "comments": comments
        },
    }


def writeTheOutputFile(dictionary : dict, outputFile : str):

    with open(outputFile, "r") as file:
        lst = json.load(file)

    with open(outputFile, mode='w') as f:
        json.dump(lst, f, ensure_ascii=False)

    with open(outputFile, mode='w') as f:
        lst.append(dictionary)
        json.dump(lst, f, ensure_ascii=False)


def doTheJob(id, outputFile):
    dictionary = createADictionnaryWithAllTheInformations(id)
    writeTheOutputFile(dictionary, outputFile)


def getTheInputFile(inputFile: str, outputFile: str):
    toto = open(inputFile, "r")
    data = json.load(toto)
    for i in data['videos_id']:
        doTheJob(i, outputFile)
    toto.close()


def readArguments(argv):
    inputFile = ''
    outputFile = ''
    try:
        options, args = getopt.getopt(argv,"hi:o:",["input=","output="])
    except getopt.GetoptError:
        print ('scrapper.py --input <inputfile> --output <outputfile>')
        sys.exit(2)
    for opt, arg in options:
        if opt == '-h':
            print ('scrapper.py --input <inputfile> --output <outputfile>')
            sys.exit()
        elif opt in ("-i", "--input"):
            inputFile = arg
        elif opt in ("-o", "--output"):
            outputFile = arg
    return inputFile, outputFile

def main():
    inputFile, outputFile =  readArguments(sys.argv[1:])
    getTheInputFile(inputFile, outputFile)

if __name__ == '__main__':
    main()

