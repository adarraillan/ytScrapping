import json

from bs4 import BeautifulSoup
import requests
import re

import time
from selenium.webdriver import Chrome#, Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


tryWithTheComments = False


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
    with Chrome() as driver:
        wait = WebDriverWait(driver, 60)
        driver.get("https://www.youtube.com/watch?v=" + video_id)

        for item in range(0):
            wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
            time.sleep(5)

        return [comment.text for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#comment #content-text")))]



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


def writeTheOutputFile(dictionary : dict):
    filename = 'output.json'

    with open(filename, "r") as file:
        lst = json.load(file)

    with open(filename, mode='w') as f:
        json.dump(lst, f, ensure_ascii=False)

    with open(filename, mode='w') as f:
        lst.append(dictionary)
        json.dump(lst, f, ensure_ascii=False)


def doTheJob(id):
    dictionary = createADictionnaryWithAllTheInformations(id)
    writeTheOutputFile(dictionary)


def getTheInputFile(inputFile: str):
    toto = open(inputFile, "r")
    data = json.load(toto)
    for i in data['videos_id']:
        doTheJob(i)
    toto.close()


def main():
    getTheInputFile('input.json')
    print('toto')

if __name__ == '__main__':
    main()

