from __future__ import unicode_literals
from bs4 import BeautifulSoup
import requests
import os
from Models import Episode, Program, Channel
    
class Parser(object):
    def __init__(self, baseUrl, url):
        self.__baseUrl = baseUrl
        self.__url = url.strip()
        
    @property
    def baseUrl(self):
        return self.__baseUrl

    @property
    def url(self):
        return self.__url
    
    @property
    def content(self):
        result = requests.get(self.url)
        return BeautifulSoup(result.content, "html.parser")
    
    def titleAndLinkFor(self, programHtml):
        urlTag = programHtml.find("a")
        return urlTag.contents[0], urlTag["href"].strip()
       
class ProgramsParser(Parser):
    def __init__(self, baseUrl, programsUrl):
        super(ProgramsParser, self).__init__(baseUrl, programsUrl)
        self.__iterator = self.programsIterator()
      
    def episodesUrl(self, programUrl):
        return os.path.join(programUrl, "capitulos").strip()
    
    @property
    def imageUrls(self):
        verticalImages = self.content.find_all("div", "views-field-field-imagen-vertical")
        smallImages = self.content.find_all("div", "views-field-field-imagen-programa")
        return verticalImages + smallImages
     
    def programsIterator(self):
        programs = self.content.find_all("div", "views-field-title") # "views-field-field-imagen-programa")
        for program, programImage in zip(programs, self.imageUrls):
            title, url = self.titleAndLinkFor(program)            
            imageUrl = programImage.find("img")["src"]
            yield Program(url, title, imageUrl, EpisodesParser(self.baseUrl, self.episodesUrl(url)))
            
    def __iter__(self):
        return self
    
    def __next__(self):
        return next(self.__iterator)
    
    def next(self):
        return self.__next__()

class EpisodesParser(Parser):
    def __init__(self, baseUrl, episodesUrl):
        super(EpisodesParser, self).__init__(baseUrl, episodesUrl)
        self.__iterator = self.episodesIterator()
        
    def fill(self, htmlParts, episodes):
        return htmlParts if len(htmlParts) > 0 else ["" for _ in range(len(episodes))]
        
    def episodesIterator(self):
        episodes = self.content.find_all("div", "views-field-title")
        episodeImages = self.content.find_all("div", "views-field-field-imagen-video")
        alternativeImages = self.content.find_all("div", "views-field-field-imagen-nota") 
        alternativeImages = self.fill(alternativeImages, episodes)
        
        episodeDescriptions = self.content.find_all("div", "views-field-field-descripcion")
        episodeDescriptions = self.fill(episodeDescriptions, episodes)
        
        for episode, episodeImage, alternativeImage, episodeDescription in zip(episodes, episodeImages, alternativeImages, episodeDescriptions):
            title, url = self.titleAndLinkFor(episode)
            imagePart = episodeImage.find("img")
            if not imagePart:
                imagePart = alternativeImage.find("img")
            imageUrl = "" if not imagePart else imagePart["src"]
            description = "" if not episodeDescription else episodeDescription.find("div", "field-content").text
            if url.startswith("/"):
                url = url[1:]
            episodeUrl = os.path.join(self.baseUrl, url)
            yield Episode(episodeUrl, title, description, imageUrl)
                  
    def __iter__(self):
        return self
    
    def __next__(self):
        return next(self.__iterator)

    def next(self):
        return self.__next__()

class RcnScraper(object):
    @property
    def baseUrl(self):
        return r"http://www.canalrcn.com/"
    
    @property
    def programsUrl(self):
        return os.path.join(self.baseUrl, "programas")
    
    @property
    def channels(self):        
        return [Channel(self.baseUrl, "RCN", ProgramsParser(self.baseUrl, self.programsUrl))]

    def channelFor(self, channelUrl):
        return Channel(self.baseUrl, "RCN", ProgramsParser(self.baseUrl, self.programsUrl))

    def programFor(self, programUrl):
        programsParser = ProgramsParser(self.baseUrl, self.programsUrl)
        for program in programsParser:
            if program.url == programUrl:
                return program
        return None

