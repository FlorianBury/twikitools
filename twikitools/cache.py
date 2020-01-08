import logging
logger = logging.getLogger(__name__)
import os, os.path

from .fetch import get_topic_raw

class RawTopicCache:
    def __init__(self, twiki_root, basepath, rawmode="debug"):
        self.twiki_root = twiki_root.rstrip("/")
        self.basepath = basepath
        if not os.path.exists(basepath):
            os.makedirs(basepath)
        if not os.path.isdir(basepath):
            raise RuntimeError("Path {0} exists, but is not a directory".format(basepath))
        self.rawmode = rawmode
    def get(self, web_topic, session=None):
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
        raw_content = get_topic_raw(session, web_topic, self.twiki_root, rawmode=self.rawmode)
        webpath = os.path.join(self.basepath, web)
        logger.debug("Storing in {0}".format(cachepath))
        if not os.path.isdir(webpath):
            os.makedirs(webpath)
        with open(cachepath, "w") as fp:
            fp.write(raw_content)
        return raw_content
