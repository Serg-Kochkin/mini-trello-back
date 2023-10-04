from app import flask_app as app
from .schema import schema
from flask_graphql import GraphQLView


app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
    'graphql',
    schema=schema,
    graphiql=True
))


@app.route('/')
def index():
    return "The server is running!"
