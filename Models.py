from __future__ import unicode_literals
from MediaStream import MediaStream
import os

class Episode(object):
    def __init__(self, url, title, description, imageUrl):
        self.__url = url
        self.__title = title
        self.__description = description
        self.__imageUrl = imageUrl
        self.__mediaStreamUrl = None
    
    @property
    def url(self):
        return self.__url
    
    @property
    def title(self):
        return self.__title
    
    @property
    def description(self):
        return self.__description
    
    @property
    def imageUrl(self):
        return self.__imageUrl

    @property
    def mediaStreamUrl(self):
        if not self.__mediaStreamUrl:
            try:
                self.__mediaStreamUrl = MediaStream().getMediaStreamUrl(self.url)
            except:
                self.__mediaStreamUrl = "Not found"
        return self.__mediaStreamUrl

    def toItem(self, plugin):
        return {"label" : self.title,
                "icon" : self.imageUrl,
                "path"  : self.mediaStreamUrl,
                "is_playable" : True
                }
   
class Program(object):
    def __init__(self, url, title, imageUrl, episodes):
        self.__url = url
        self.__title = title
        self.__imageUrl = imageUrl
        self.__episodes = episodes
        
    @property
    def url(self):
        return self.__url
    
    @property
    def title(self):
        return self.__title
    
    @property
    def imageUrl(self):
        return self.__imageUrl
    
    @property
    def episodes(self):
        return self.__episodes

    def toItem(self, plugin):
        return {"label" : self.title,
                "path"  : plugin.url_for("show_episodes", programUrl=self.url
                    ) ,

                "icon" : self.imageUrl,
                "is_playable" : False
                }

class Channel(object):
    def __init__(self, url, name, programs):
        self.__url = url
        self.__name = name
        self.__programs = programs
    
    @property
    def url(self):
        return self.__url
    
    @property    
    def name(self):
        return self.__name
    
    @property
    def programs(self):
        return self.__programs
   
    def toItem(self, plugin):
        return {"label" : self.name,
                "path"  : plugin.url_for("show_programs", channelUrl=self.url) ,
                "is_playable" : False
                }
