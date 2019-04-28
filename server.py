import wikipediaapi
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    data = request.json
    if data['api'] == 'geocoder':
        links = {'a': 'https://google.com'}

        toponym = data['response']
        address = toponym['metaDataProperty']['GeocoderMetaData']['text']

    elif data['api'] == 'geosearch':
        links = {'a': 'https://google.com'}
        organization = data['response']
        address = organization['properties']['CompanyMetaData'].get('address')
        url = organization['properties']['CompanyMetaData'].get('url')

    return render_template('index.html', links=links)


@app.route('/information')
def info():
    return render_template('info.html')


@app.route('/wiki/<wiki_request>')
def wiki(wiki_request):
    wiki_wiki = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.HTML)
    p_wiki = wiki_wiki.page(wiki_request)

    return p_wiki.text


@app.route('/help')
def docs():
    return render_template('manual.html')


if __name__ == 'server':
    app.run(host='127.0.0.1', port=8080)
