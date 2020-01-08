""" Helper methods for parsing twiki source and html pages """

def _getStr(results, default=""):
    if len(results) > 0:
        return results[0].string
    else:
        return default

def _getAttr(results, attName, default=""):
    if len(results) > 0:
        return results[0][attName]
    else:
        return default

def webindex_entries(webindex_soup):
    """
    Iterator that gets the data out of a webindex html page

    :param webindex_soup: BeautifulSoup of the WebIndex html page

    :yields: ``("Web.Topic", "revision", "author_name", "summary")``
    """
    for elem in webindex_soup.find_all("div", class_="patternSearchResult"):
        href = _getAttr(elem.select("div.twikiTopRow > a"), "href")
        web, topic = tuple(href.split("/")[-2:])
        rev = _getStr(elem.select("span.twikiSRRev > a"))
        author = _getStr(elem.select("span.twikiSRAuthor > a"))
        summary = _getStr(elem.select("div.twikiSummary"))
        yield ("{web}.{topic}".format(web=web, topic=topic), rev, author, summary)
