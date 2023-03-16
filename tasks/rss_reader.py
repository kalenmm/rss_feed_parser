# Importing json for formatting dicts to json
import json as js
# importing feedparser module for parsing XML from Web
import feedparser
# ArgumentParser for cmd execution
from argparse import ArgumentParser
# this module is used to support type annotations
from typing import List, Optional, Sequence
# Importing module request for HTTP requests
import requests


# By this class we catch unhandled exceptions
class UnhandledException(Exception):
    pass


# Function for parsing our xml request
# Args:
# xml: XML document as a string.
# --limit: Number of the news to return. if None, returns all news.
# --json: If True, format output as JSON.
def rss_parser(
        xml: str,
        limit: Optional[int] = None,
        json: bool = False,
) -> List[str]:
    # returning list of result
    result = []
    # feed used for parsing xml request
    feed = feedparser.parse(xml)

    # --limit -> Specifying limitations
    limitation = limit
    if limitation is not None:
        if limitation > len(feed.entries):
            limitation = len(feed.entries)
        else:
            limitation = limit
    else:
        limitation = len(feed.entries)

    # Making shortcuts for feed and entries of our xml
    f = feed.feed
    e = feed.entries

    items = []
    dict_temp = {
                 "title": f.title,
                 "link": f.link,
                 "description": f.subtitle
                 }

    # --json -> if json is True formats output to json
    if json is True:
        for i in range(0, limitation):
            items.append({
                "title": e[i].title,
                "pubDate": e[i].published,
                "link": e[i].link,
                # Maybe to change source to description or to subtitle
                "description": e[i].source.title
            })
        dict_temp["items"] = items
        json_temp = js.dumps(dict_temp)
        print(json_temp, "HERE")
        for key, value in dict_temp.items():
            result.append(f"{str(key)}: {str(value)}")
    else:
        dict_temp['Feed'] = dict_temp['title']
        dict_temp['Link'] = dict_temp['link']
        dict_temp['Description'] = dict_temp['description']
        del dict_temp['title']
        del dict_temp["link"]
        del dict_temp['description']
        for i in range(0, limitation):
            items.append({
                "Title": e[i].title,
                "Published": e[i].published,
                "Link": e[i].link,
                "Description": e[i].source.title
            })
        dict_temp['items'] = items
        for key, value in dict_temp.items():
            result.append(f"{str(key)}: {str(value)}")
        return result
    """
    Returns:
        List of strings.
        Which then can be printed to stdout or written to file as a separate lines.

    Examples:
        >>> xml = '<rss><channel><title>Some RSS Channel</title><link>https://some.rss.com</link><description>Some RSS 
        Channel</description></channel></rss>'
        >>> rss_parser(xml)
        ["Feed: Some RSS Channel",
        "Link: https://some.rss.com"]
        >>> print("\\n".join(rss_parser(xmls)))
        Feed: Some RSS Channel
        Link: https://some.rss.com
    """


def main(argv: Optional[Sequence] = None):
    """
    The main function of task.
    parser -> arg parsing our xml requests from cmd
    """
    parser = ArgumentParser(
        prog="rss_reader",
        description="Pure Python command-line RSS reader.",
    )
    parser.add_argument("source", help="RSS URL", type=str, nargs="?")
    parser.add_argument(
        "--json", help="Print result as JSON in stdout", action="store_true"
    )
    parser.add_argument(
        "--limit", help="Limit news topics if this parameter provided", type=int
    )

    args = parser.parse_args(argv)
    xml = requests.get(args.source).text
    try:
        print("\n".join(rss_parser(xml, args.limit, args.json)))
        return 0
    except Exception as e:
        raise UnhandledException(e)


if __name__ == "__main__":
    main()
    # You can try the links below
    # xml1 = "https://news.yahoo.com/rss"
    # xml2 = "<rss><channel><title>Some RSS Channel</title><link>https://some.rss.com</link>
    # <description>Some RSS Channel2</description></channel></rss>"
    # print("\n".join(rss_parser(xml1, limit=2, json=False)))
    # print(rss_parser(xml2, json=False, limit=2))
