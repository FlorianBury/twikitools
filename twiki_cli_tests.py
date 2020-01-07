#!/usr/bin/env python
import logging
logger = logging.getLogger(__name__)
import os.path
import pickle
import requests
import cern_sso

def get_cookiejar(loginUrl, cookieFile=None):
    if cookieFile:
        try:
            with open(cookieFile, "rb") as f:
                cookieJar = pickle.load(f)
            with requests.Session() as s:
                s.cookies = cookieJar
                r1 = s.get(loginUrl, timeout=cern_sso.DEFAULT_TIMEOUT_SECONDS)
                if r1.url == loginUrl:
                    logging.debug("SSO cookie from {0} is still valid".format(cookieFile))
                    return cookieJar
        except IOError as ex:
            logger.exception(ex)
    cookieJar = cern_sso.krb_sign_on(loginUrl)
    with open(cookieFile, "wb") as f:
        pickle.dump(cookieJar, f)
    return cookieJar

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Play a bit with requests and CERN SSO")
    parser.add_argument("--login-url", default="https://twiki.cern.ch/twiki/bin/view/CMS/WebHome", help="URL to use for authentication (with SSO and kerberos)")
    parser.add_argument("--cookie-jar", default=os.path.join(os.path.dirname(__file__), ".cookies"), help="File to save cookies to")
    parser.add_argument("--root", default="https://twiki.cern.ch/twiki/bin/", help="Twiki server root (up to (cgi-)bin/)")
    parser.add_argument("--dumpdebug", default=[], action="append", help="Topics (in Web.TopicName format) to dump (in raw=debug mode)")
    parser.add_argument("--dumpheaders", default=[], action="append", help="Topics (in Web.TopicName format) to dump the headers of")
    parser.add_argument("-v", "--verbose", action="store_true", help="Debug/verbose mode")
    args = parser.parse_args()

    logging.basicConfig(level=(logging.DEBUG if args.verbose else logging.INFO))

    cookiejar = get_cookiejar(args.login_url, args.cookie_jar)

    logger.info("Your SSO cookies are ready - have fun!")

    resp = []
    with requests.Session() as s:
        s.cookies = cookiejar
        for toDump in args.dumpdebug:
            web,topic = toDump.split(".")
            rd = s.get("{0}/view/{web}/{topic}?skin=text&raw=debug&contenttype=text/plain".format(args.root, web=web, topic=topic), timeout=cern_sso.DEFAULT_TIMEOUT_SECONDS)
            contents = rd.content.decode(rd.apparent_encoding)
            logging.info("Contents of {0}:".format(toDump))
            print("\n{0}\n\n".format(contents))
        for toDump in args.dumpheaders:
            web,topic = toDump.split(".")
            rd = s.get("{0}/view/{web}/{topic}?skin=text&raw=debug&contenttype=text/plain".format(args.root, web=web, topic=topic), timeout=cern_sso.DEFAULT_TIMEOUT_SECONDS)
            contents = rd.content.decode(rd.apparent_encoding)
            logging.info("Headers of {0}:".format(toDump))
            print("\n".join(ln.strip().lstrip("-") for ln in contents.split("\n") if ln.lstrip().startswith("---"))) ## only twiki headers
