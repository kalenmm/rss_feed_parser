# You shouldn't change  name of function or their arguments
# but you can change content of the initial functions.
import json as js
import feedparser
from argparse import ArgumentParser
from typing import List, Optional, Sequence
import requests


class UnhandledException(Exception):
    pass


def rss_parser(
    xml: str,
    limit: Optional[int] = None,
    json: bool = False,
) -> List[str]:
    # feed = feedparser.parse('https://www.upwork.com/ab/feed/jobs/rss?q=web+scraper&sort=recency&paging=0%3B10&api_params=1&securityToken=b81cd9281c89f630d0c13022476f3bea26d22c5590013ab4f43c4e390c86a52d69ff5876be0a6d7b174b8888dab7e7aaa59cd884c771490d6f4c09b0d3b903b2&userUid=955976492232273920&orgUid=955976492236468225')
    result = []
    feed = feedparser.parse(xml)

    # Specifying limitations
    limitation = limit
    if limitation is not None:
        if limitation > len(feed.entries):
            limitation = len(feed.entries)
        else:
            limitation = limit
    else:
        limitation = len(feed.entries)

    # Making shortcuts
    f = feed.feed
    e = feed.entries

    # Making short forms
    title_feed = f.title
    link_feed = f.link
    description_feed = f.subtitle
    items = []
    dict_temp = {"title": title_feed,
                 "link": link_feed,
                 "description": description_feed
                 }

    # If it's requested json
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
        return result
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
    RSS parser.

    Args:
        xml: XML document as a string.
        limit: Number of the news to return. if None, returns all news.
        json: If True, format output as JSON.

    Returns:
        List of strings.
        Which then can be printed to stdout or written to file as a separate lines.

    Examples:
        >>> xml = '<rss><channel><title>Some RSS Channel</title><link>https://some.rss.com</link><description>Some RSS Channel</description></channel></rss>'
        >>> rss_parser(xml)
        ["Feed: Some RSS Channel",
        "Link: https://some.rss.com"]
        >>> print("\\n".join(rss_parser(xmls)))
        Feed: Some RSS Channel
        Link: https://some.rss.com
    """



def main(argv: Optional[Sequence] = None):
    """
    The main function of your task.
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
    # xml2 = "https://news.yahoo.com/rss"
    # xml = "<rss><channel><title>Some RSS Channel</title><link>https://some.rss.com</link><description>Some RSS Channel2</description></channel></rss>"
    # print("\n".join(rss_parser(xml2, limit=2, json=False)))
    # print(rss_parser(xml2, json=False, limit=2))
