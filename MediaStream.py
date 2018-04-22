from bs4 import BeautifulSoup
import requests

class MediaStream(object):
    def parseUrlContent(self, url):
        result = requests.get(url)
        return BeautifulSoup(result.content, "html.parser")

    def getVideoFrameUrl(self, episodeUrl):
        result = self.parseUrlContent(episodeUrl)
        videoFrames = [frame for frame in result.find_all("iframe") if frame.has_attr("allowfullscreen")]
        return r"https:" + videoFrames[0].get("src")

    def getMediaStreamUrl(self, episodeUrl):
        videoFrameUrl = self.getVideoFrameUrl(episodeUrl)
        soup = self.parseUrlContent(videoFrameUrl)
        metaUrls = [meta.get("content") for meta in soup.find_all("meta") if meta.get("content") and meta.get("property") and meta["property"] == "og:video:url" and meta["content"].endswith(".m3u8") and "swf" not in meta["content"]]
        return metaUrls[0]
