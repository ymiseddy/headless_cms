import datetime
import json
import cerberus
from krnch.eventstore import EventStore, DataEntity, attribute, datetimeattribute
from krnch.tools import new_id
from krnch.routing import service, handles
import cms.base_commands as bc


def _to_date(str_format):
    return datetime.datetime.strptime(str_format, "%Y-%m-%d %H:%M:%S")

def _automap(instance, struct):
    for key, value in struct.items():
        if hasattr(instance, key):
            setattr(instance, key, value)


class ArticleAddCommand(bc.ValidatingCommand):
    """ Command that adds a new article. """
    schema = {
        "title": {"type": "string", "required": True, "minlength": 2, "maxlength": 45},
        "summary": {"type": "string", "required": True, "minlength": 2, "maxlength": 512},
        "author": {"type": "string", "required": True, "minlength": 2, "maxlength": 45},
        "release_date": {"type": "datetime", "required": True, "coerce": _to_date},
        "body": {"type": "string", "required": True, "minlength": 2}
    }

class ArticleUpdateCommand(bc.ValidatingCommand):
    schema = {
        "id": {"type": "string", "required": True},
        "title": {"type": "string", "required": False, "minlength": 2, "maxlength": 45},
        "summary": {"type": "string", "required": False, "minlength": 2, "maxlength": 512},
        "author": {"type": "string", "required": False, "minlength": 2, "maxlength": 45},
        "release_date": {"type": "datetime", "required": False, "coerce": _to_date},
        "body": {"type": "string", "required": False, "minlength": 2}
    }

class ArticleDeleteCommand:
    pass

class ArticleListQuery:
    pass

class ArticleGetQuery(bc.ValidatingCommand):
    schema = {
        "id": {"type": "string", "required": True}
    }

class Article(DataEntity):
    title = attribute()
    summary = attribute()
    author = attribute()
    release_date = datetimeattribute()
    body = attribute()


@service
class ArticleManager:

    def __init__(self, eventstore: EventStore):
        self.eventstore = eventstore

    @handles(ArticleAddCommand)
    def handle_article_add(self, cmd):
        """ Adds a new article. """
        with self.eventstore.context() as ctx:
            entity_id = new_id()
            article = ctx.new(Article, entity_id)
            _automap(article, cmd.struct)
            article.save()
            return bc.DispatchResponse(bc.SUCCESS, article.entity_id)

    @handles(ArticleUpdateCommand)
    def handle_article_update(self, cmd):
        """ Updates an existing article. """
        with self.eventstore.context() as ctx:
            entity_id = cmd.id
            article = ctx.load(Article, entity_id)
            _automap(article, cmd.struct)
            article.save()
            return article.entity_id



    @handles(ArticleGetQuery)
    def handle_article_get(self, cmd):
        """ Retrieves an existing article. """
        with self.eventstore.readonly_context() as ctx:
            entity_id = cmd.id
            article = ctx.load(Article, entity_id)
            return article.state
