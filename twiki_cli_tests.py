#!/usr/bin/env python
import logging
logger = logging.getLogger(__name__)
import os.path
import requests

from twikitools.cern_sso import get_sso_cookiejar, DEFAULT_TIMEOUT_SECONDS
from twikitools.fetch import get_topic_raw
from twikitools.cache import RawTopicCache

import tempfile
from contextlib import contextmanager
@contextmanager
def empty_context(toYield):
    yield toYield

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Play a bit with requests and CERN SSO")
    parser.add_argument("--login-url", default="https://twiki.cern.ch/twiki/bin/view/CMS/WebHome", help="URL to use for authentication (with SSO and kerberos)")
    parser.add_argument("--cookie-jar", default=os.path.join(os.path.dirname(__file__), ".cookies"), help="File to save cookies to")
    parser.add_argument("--root", default="https://twiki.cern.ch/twiki/bin/", help="Twiki server root (up to (cgi-)bin/)")
    parser.add_argument("--cache", default=None, help="Cache directory for topic sources (if not specified, a temporary directory will be used)")
    parser.add_argument("--dumpdebug", default=[], action="append", help="Topics (in Web.TopicName format) to dump (in raw=debug mode)")
    parser.add_argument("--dumpheaders", default=[], action="append", help="Topics (in Web.TopicName format) to dump the headers of")
    parser.add_argument("-v", "--verbose", action="store_true", help="Debug/verbose mode")
    args = parser.parse_args()

    logging.basicConfig(level=(logging.DEBUG if args.verbose else logging.INFO))

    sso_cookiejar = get_sso_cookiejar(args.login_url, args.cookie_jar)

    logger.info("Your SSO cookies are ready - have fun!")

    resp = []
    with requests.Session() as s:
        s.cookies = sso_cookiejar
        with (empty_context(args.cache) if args.cache else tempfile.TemporaryDirectory()) as cachedir:
            rawCache = RawTopicCache(args.root, cachedir)
            for toDump in args.dumpdebug:
                contents = rawCache.get(toDump, session=s)
                logging.info("Contents of {0}:".format(toDump))
                print("\n{0}\n\n".format(contents))
            for toDump in args.dumpheaders:
                contents = rawCache.get(toDump, session=s)
                logging.info("Headers of {0}:".format(toDump))
                print("\n".join(ln.strip().lstrip("-") for ln in contents.split("\n") if ln.lstrip().startswith("---"))) ## only twiki headers
