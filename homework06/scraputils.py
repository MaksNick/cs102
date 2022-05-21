import requests  # type: ignore
from bs4 import BeautifulSoup


def extract_news(parser):
    """Extract news from a given web page"""
    news_list = []
    list_of_news = parser.findAll("tr", class_="athing")
    list_of_subtext = parser.findAll("td", class_="subtext")
    for news, subtext in zip(list_of_news, list_of_subtext):
        dictionary = {}
        temp = news.findAll("td", class_="title")[1]
        dictionary["author"] = subtext.findAll("a", class_="hnuser")[0].text
        dictionary["comments"] = int(subtext.text.split("|")[-1].strip().replace("discuss", "0")[0])
        dictionary["points"] = int(subtext.findAll("span", class_="score")[0].text[0])
        dictionary["title"] = temp.findAll("a", class_="titlelink")[0].text
        dictionary["url"] = temp.findAll("a", class_="titlelink")[0].get("href")
        news_list.append(dictionary)
    return news_list


def extract_next_page(parser):
    """Extract next page URL"""
    next_page = parser.findAll("a", class_="morelink")
    return next_page[0].get("href")


def get_news(url, n_pages=1):
    """Collect news from a given web page"""
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news
