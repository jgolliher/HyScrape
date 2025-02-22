from typing import List
import urllib.parse
import requests as rq
from bs4 import BeautifulSoup


def get_meet_events(url: str) -> List:
    """Return a list of event names and URLs

    Args:
        url (str): The URL to get meet information from

    Returns:
        List: A list containing event name and HTML file name
    """
    if "evtindex.htm" not in url:
        url = urllib.parse.urljoin(url, "evtindex.htm")
    response = rq.get(url)
    if response.status_code != 200:
        raise ValueError(f"Invalid response code {response.status_code}")
    content = BeautifulSoup(response.content, features="html.parser")
    events = content.find_all("a", href=True)
    events = [event for event in events if event.text.startswith("#")]
    events = [[event.text, event["href"]] for event in events]
    return events
