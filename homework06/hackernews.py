import string

from bottle import route, run, template, request, redirect

import nltk
from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier
import os

nltk.download("punkt")


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    label = request.query.label
    record = s.query(News).filter(News.id == request.query.id).all()[0]
    record.label = label
    s.add(record)
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    list_of_news = get_news("https://news.ycombinator.com/newest", n_pages=5)
    s = session()
    for new in list_of_news:
        if (
            s.query(News)
            .filter(News.title == new["title"] and News.author == new["author"])
            .first()
            is None
        ):
            news = News(
                title=new["title"],
                author=new["author"],
                url=new["url"],
                comments=new["comments"],
                points=new["points"],
                label=None,
            )
            s.add(news)
    s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    classified_news, maybe, bad = [], [], []
    labeled = s.query(News).filter(News.label != None).all()
    bayes = NaiveBayesClassifier()
    x, y = [
        nltk.word_tokenize(
            item.title.translate(str.maketrans("", "", string.punctuation))
        )
        for item in labeled
    ], [item.label for item in labeled]
    bayes.fit(x[: len(x) * 7 // 10], y[: len(y) * 7 // 10])
    print(bayes.score(x[len(x) * 7 // 10 :], y[len(y) * 7 // 10 :]))
    unlabeled = s.query(News).filter(News.label == None).all()
    predict = bayes.predict(
        [
            nltk.word_tokenize(
                item.title.translate(str.maketrans("", "", string.punctuation))
            )
            for item in unlabeled
        ]
    )
    for i, item in enumerate(unlabeled):
        if predict[i] == "good":
            classified_news.append(item)
        elif predict[i] == "maybe":
            maybe.append(item)
        else:
            bad.append(item)
    classified_news.extend(maybe)
    classified_news.extend(bad)
    return template("news_recommendations", rows=classified_news)


if __name__ == "__main__":
    run(host="localhost", port=8080)
