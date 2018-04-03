from bs4 import BeautifulSoup
import requests
import os

baseUrl = r"http://www.canalrcn.com/"

def parseUrlContent(url):
    result = requests.get(url)
    return BeautifulSoup(result.content, "html.parser")

def programsUrl():
    return os.path.join(baseUrl, "programas")

def episodesUrl(programUrl):
    return os.path.join(programUrl, "capitulos")

def titleAndLinkFor(programHtml):
    urlTag = programHtml.find("a")
    return urlTag.contents[0], urlTag["href"]

def episodesFor(episodesUrl):
    parsedEpisodes = parseUrlContent(episodesUrl)
    episodes = parsedEpisodes.find_all("div", "views-field-title")
    for episode in episodes:
        title, url = titleAndLinkFor(episode)
        print("   {}: {}".format(title, url))

soup = parseUrlContent(programsUrl())

programs = soup.find_all("div", "views-field-title") # "views-field-field-imagen-programa")
for program in programs:
    title, url = titleAndLinkFor(program)
    print("{}: {}".format(title, url))
    episodesFor(episodesUrl(url))





