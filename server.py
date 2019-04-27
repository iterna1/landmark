import wikipediaapi
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/<wiki_request>', methods=['GET'])
def index(wiki_request):
    wiki_wiki = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.HTML )
    p_wiki = wiki_wiki.page(wiki_request)

    return p_wiki.text


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
