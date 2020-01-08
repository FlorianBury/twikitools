import logging
logger = logging.getLogger(__name__)
import os, os.path

from .fetch import get_topic_raw, get_topic_webbacklinks, DEFAULT_TIMEOUT_SECONDS

class PerTopicCache:
    def __init__(self, twiki_root, basepath, timeout=DEFAULT_TIMEOUT_SECONDS):
        self.twiki_root = twiki_root.rstrip("/")
        self.basepath = basepath
        if not os.path.exists(basepath):
            os.makedirs(basepath)
        if not os.path.isdir(basepath):
            raise RuntimeError("Path {0} exists, but is not a directory".format(basepath))
        self.timeout = timeout
    def get(self, web_topic, session=None, timeout=None):
        web,topic = web_topic.split(".")
        cachepath = os.path.join(self.basepath, web, topic)
        if os.path.exists(cachepath):
            try:
                logger.debug("Reading from {0}".format(cachepath))
                with open(cachepath) as fp:
                    return fp.read()
            except IOError as ex:
                logger.error("Problem while reading from file {0} (details follow), refetching".format(cachepath))
                logger.exception(ex)
        ## fetch
        raw_content = self.fetch(web_topic, session=session, timeout=timeout)
        webpath = os.path.join(self.basepath, web)
        logger.debug("Storing in {0}".format(cachepath))
        if not os.path.isdir(webpath):
            os.makedirs(webpath)
        with open(cachepath, "w") as fp:
            fp.write(raw_content)
        return raw_content
    def fetch(self, web_topic, session=None, timeout=None):
        pass ## interface method

class RawTopicCache(PerTopicCache):
    def __init__(self, twiki_root, basepath, rawmode="debug", timeout=DEFAULT_TIMEOUT_SECONDS):
        super(RawTopicCache, self).__init__(twiki_root, basepath, timeout=timeout)
        self.rawmode = rawmode
    def fetch(self, web_topic, session=None, timeout=None):
        return get_topic_raw(session, web_topic, self.twiki_root, timeout=(timeout if timeout else self.timeout), rawmode=self.rawmode)

class WebBacklinksCache(PerTopicCache):
    def __init__(self, twiki_root, basepath, timeout=DEFAULT_TIMEOUT_SECONDS):
        super(WebBacklinksCache, self).__init__(twiki_root, basepath, timeout=timeout)
    def fetch(self, web_topic, session=None, timeout=None):
        return get_topic_webbacklinks(session, web_topic, self.twiki_root, timeout=(timeout if timeout else self.timeout))
