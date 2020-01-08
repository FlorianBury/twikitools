#!/usr/bin/env python
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert a search results (e.g. WebIndex, backlinks) html page to csv (tab-separated plain text, printed to stdout)")
    parser.add_argument("webindex.html", help="Path of the (locally saved) html page")
    parser.add_argument("--encoding", default=None, help="Encoding of the html file")
    args = parser.parse_args()

    from bs4 import BeautifulSoup
    from twikitools.parse import searchresults_entries
    with open(getattr(args, "webindex.html"), encoding=args.encoding) as fp:
        soup = BeautifulSoup(fp, "lxml")
        for web_topic, rev, author, summary in searchresults_entries(soup):
            print("{webtopic:<35}{rev:<20}{author:<25}{summary}".format(webtopic=web_topic, rev=rev, author=author, summary=(summary[:80] if summary else "")))
