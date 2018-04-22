class MediaStream(object):
    def getVideoFrameUrl(self, episodeUrl):
        result = parseUrlContent(episodeUrl)
        videoFrames = [frame for frame in result.find_all("iframe") if frame.has_attr("allowfullscreen")]
        return r"https:" + videoFrames[0].get("src")

    def getMediaStreamUrl(episodeUrl):
        videoFrameUrl = self.getVideoFrameUrl(episodeUrl)
        soup = parseUrlContent(videoFrameUrl)
        metaUrls = [meta.get("content") for meta in soup.find_all("meta") if meta.get("content") and meta.get("property") and meta["property"] == "og:video:url" and meta["content"].endswith(".m3u8") and "swf" not in meta["content"]]
        return metaUrls[0]
