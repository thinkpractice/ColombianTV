from bs4 import BeautifulSoup
import requests
import m3u8

class MediaStream(object):
    def parseUrlContent(self, url):
        result = requests.get(url)
        return BeautifulSoup(result.content, "html.parser")

    def getVideoFrameUrl(self, episodeHtml):
        videoFrames = [frame for frame in episodeHtml.find_all("iframe") if frame.has_attr("allowfullscreen")]
        if len(videoFrames) == 0:
            return ""
        return r"https:" + videoFrames[0].get("src")

    def parsePlaylistForStreams(self, playlistUrl):
        m3u8_obj = m3u8.load(playlistUrl)
        return {playlist.stream_info.bandwidth : playlist.uri for playlist in m3u8_obj.playlists}

    def bestStreamFor(self, playlistUrl):
        #streamsDict = self.parsePlaylistForStreams(playlistUrl)
        #bestQualityKey = sorted(streamsDict.keys(), reverse=True)[0]
        #return streamsDict[bestQualityKey]
        return playlistUrl.replace("m3u8", "mp4")

    def getMediaStreamUrl(self, episodeUrl):
        result = self.parseUrlContent(episodeUrl)
        videoFrameUrl = self.getVideoFrameUrl(result)        
        if not videoFrameUrl:                 
            videoId = result.find("input", {"id" : "vd_id"})
            if not videoId:           
                raise Exception("Video url not found for episode {}".format(episodeUrl))
            return "https://mdstrm.com/video/{}.mp4".format(videoId["value"])
           
        soup = self.parseUrlContent(videoFrameUrl)
        metaUrls = [meta.get("content") for meta in soup.find_all("meta") if meta.get("content") and meta.get("property") and meta["property"] == "og:video:url" and meta["content"].endswith(".m3u8") and "swf" not in meta["content"]]
        return self.bestStreamFor(metaUrls[0])
