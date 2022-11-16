# -*- coding: utf-8 -*-


import scrapper
import requests
from bs4 import BeautifulSoup
import re
import json as json

response=requests.get("https://www.youtube.com/watch?v=fmsoym8I-3o")
soup = BeautifulSoup(response.text,"html.parser")

def test_getRequestedUrl():
    assert scrapper.getTheRequestedUrl("fmsoym8I-3o").status_code == 200

def test_transformVideoIntoSoup():
    assert type(scrapper.transformTheVideoIntoSoup("fmsoym8I-3o")) == BeautifulSoup

def test_getVideoTitle():
    assert scrapper.getTheVideoTitle(soup) == "Pierre Niney : L’interview face cachée par HugoDécrypte"

def test_getVideoViews():
    assert scrapper.getTheVideoViews(soup) >= "738000"

def test_getVideoId():
    assert scrapper.getTheVideoId(soup) == "fmsoym8I-3o"

def test_getVideoDescription():
    assert isinstance(scrapper.getTheVideoDescription(soup), str)

#test getVideoChannelName
def test_getVideoChannelName():
    assert scrapper.getTheVideoChannelName(soup) == "HugoDécrypte"

def test_getVideoNumberOfLikes():
    assert scrapper.getTheVideoNumberOfLikes(soup) >= "0"

def test_getExternalLinksWithinVideoDescription():
    assert isinstance(scrapper.getTheExternalLinksWithinVideoDescription(soup), list)

def test_getVideoComments():
    assert isinstance(scrapper.getTheVideoComments("fmsoym8I-3o"), list)

def test_createADictionnaryWithAllTheInformations():
    assert isinstance(scrapper.createADictionnaryWithAllTheInformations("fmsoym8I-3o"), dict)

def test_writeTheOutputFile():
    scrapper.writeTheOutputFile("fmsoym8I-3o", 'output.json')
    assert open('output.json', 'r')

def test_doTheJob():
    scrapper.doTheJob("fmsoym8I-3o", 'output.json')
    assert open('output.json', 'r')
    assert isinstance(scrapper.createADictionnaryWithAllTheInformations('fmsoym8I-3o'), dict)

