import logging
logger = logging.getLogger(__name__)
import pickle
import requests
import cern_sso
from cern_sso import DEFAULT_TIMEOUT_SECONDS

def get_sso_cookiejar(loginUrl, cookieFile=None):
    """
    Helper method to login and get an SSO cookie (if needed).

    If SSO login with the coookies from ``cookieFile`` works,
    no new authentication is done.
    If a new authentication is needed, the resulting cookie jar
    is stored in ``cookieFile``

    :param loginurl: URL to use for login (i.e. any protected url)
    :param cookieFile: path of a file with a pickled requests cookie jar

    :returns: the resulting cookie jar (with valid SSO cookie)
    """
    if cookieFile:
        try:
            with open(cookieFile, "rb") as f:
                cookieJar = pickle.load(f)
            with requests.Session() as s:
                s.cookies = cookieJar
                r1 = s.get(loginUrl, timeout=DEFAULT_TIMEOUT_SECONDS)
                if r1.url == loginUrl:
                    logging.debug("SSO cookie from {0} is still valid".format(cookieFile))
                    return cookieJar
        except IOError as ex:
            logger.exception(ex)
    cookieJar = cern_sso.krb_sign_on(loginUrl)
    with open(cookieFile, "wb") as f:
        pickle.dump(cookieJar, f)
    return cookieJar

