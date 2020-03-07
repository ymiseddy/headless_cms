import setup
import sys
from krnch.eventstore import EventStore
from cms.article_management import ArticleAddCommand, ArticleGetQuery, ArticleUpdateCommand
import cms.base_commands as bc
from krnch.routing import Bus
from krnch.container import get_container

import cerberus
import json
import sys
import datetime


if __name__ == "__main__":
    article = {
        "title": "Click Here to Find Out",
        "summary": "Just click it already.",
        "author": "Bill Bob Smith",
        "release_date": "2020-03-10 12:00:00",
        "body": "This is the most clickbait article ever."
    }

    try:
        container = get_container()
        bus = container.get(Bus)
        cmd = ArticleAddCommand(article)
        response = bus.dispatch(cmd)
        print(response.result)
        exit(0)
        cmd = ArticleGetQuery({"id": "3tkvx2S5zR2Z1jLqRPFxHUe9uMFB"})
        #cmd = ArticleGetQuery({"id": "3tkvx2S5zR2Z1jLqRPFxHUe9uMF9"})
        #cmd = ArticleUpdateCommand({"id": "3tkvx2S5zR2Z1jLqRPFxHUe9uMF9", "title": "A really clicbait article"})
        #bus.dispatch(cmd)
        #exit(0)

        #es = container.get(EventStore)
        #es.initialize_storage()
        res = bus.dispatch(cmd)
        print(res)
    except bc.ValidationError as e:
        print(e.errors)
