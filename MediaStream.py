from bs4 import BeautifulSoup
import requests
import m3u8

class MediaStream(object):
    def parseUrlContent(self, url):
        result = requests.get(url)
        return BeautifulSoup(result.content, "html.parser")

    def getVideoFrameUrl(self, episodeUrl):
        result = self.parseUrlContent(episodeUrl)
        videoFrames = [frame for frame in result.find_all("iframe") if frame.has_attr("allowfullscreen")]
        return r"https:" + videoFrames[0].get("src")

    def parsePlaylistForStreams(self, playlistUrl):
        m3u8_obj = m3u8.load('https://mdstrm.com/video/5ada9b4dfa4c93132a0ea4e5.m3u8')
        return {playlist.stream_info.bandwidth : playlist.uri for playlist in m3u8_obj.playlists}

    def bestStreamFor(self, playlistUrl):
        streamsDict = self.parsePlaylistForStreams(playlistUrl)
        bestQualityKey = sorted(streamsDict.keys(), reverse=True)[0]
        return streamsDict[bestQualityKey]

    def getMediaStreamUrl(self, episodeUrl):
        videoFrameUrl = self.getVideoFrameUrl(episodeUrl)
        soup = self.parseUrlContent(videoFrameUrl)
        metaUrls = [meta.get("content") for meta in soup.find_all("meta") if meta.get("content") and meta.get("property") and meta["property"] == "og:video:url" and meta["content"].endswith(".m3u8") and "swf" not in meta["content"]]
        return self.bestStreamFor(metaUrls[0])


