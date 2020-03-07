"""
Main service.
"""
import cherrypy as cp
from bottle import Bottle, template, request, static_file

app = Bottle()

class AddArticleCommand:
    def __init__(self, author_id,
                 author_name,
                 release_date,
                 title,
                 summary,
                 tags,
                 body):
        self.author_id = author_id
        self.author_name = author_name
        self.release_date = release_date
        self.title = title
        self.summary = summary
        self.tags = tags
        self.body = body

@app.route("/test/")
def handle_test():
    return {"message": "I got it."}

def run_in_cp_tree(app, host='0.0.0.0', port=8081, **config):
    """ Run application in a cherrypy tree """
    cp.tree.graft(app, '/')
    cp.config.update(config)
    cp.config.update({
        'server.socket_port': port,
        'server.socket_host': host
    })
    cp.engine.signals.subscribe() # optional
    cp.engine.start()
    cp.engine.block()

if __name__ == "__main__":
    pass
    # run_in_cp_tree(app)
