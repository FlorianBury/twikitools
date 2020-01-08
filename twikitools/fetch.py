""" Helper methods to fetch topics, backlinks etc. from twiki """

from .cern_sso import DEFAULT_TIMEOUT_SECONDS

def get_topic_raw(session, web_topic, twiki_root, timeout=DEFAULT_TIMEOUT_SECONDS, rawmode="debug"):
    """ Get the source of a twiki topic

    :param session: requests session to use (if the web is protected: with SSO cookie)
    :param web_topic: topic name, including web, e.g. ``Main.WebHome``
    :param twiki_root: twiki server root (up to (cgi-)bin/))
    :param timeout: timeout for the request
    :param rawmode: value of the ``raw`` parameter of the request ("debug" by default, to include the metadata)
    """
    web,topic = web_topic.split(".")
    rd = session.get("{0}/view/{web}/{topic}?skin=text&raw=debug&contenttype=text/plain".format(twiki_root.rstrip("/"), web=web, topic=topic), timeout=DEFAULT_TIMEOUT_SECONDS)
    return rd.content.decode(rd.apparent_encoding)
