import wikipediaapi
from flask import Flask, render_template, request

app = Flask(__name__)
app.templates_auto_reload = True


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    data = request.json
    links = {}
    if data['api'] == 'geocoder':
        toponym = data['response']
        try:
            address = ('Address', toponym['metaDataProperty']['GeocoderMetaData']['text'])
        except KeyError:
            address = ('Address', None)
        try:
            postal_code = ('Postal code', toponym['metaDataProperty']['GeocoderMetaData']['Address'].get('postal_code'))
        except KeyError:
            postal_code = ('Postal code', None)
        try:
            point = ('Point', toponym['Point']['pos'])
        except KeyError:
            point = ('Point', None)
        try:
            address_components = []
            for i in toponym['metaDataProperty']['GeocoderMetaData']['Address']['Components']:
                if i['kind'] in ('locality', 'province', 'country'):
                    address_components.append((i['kind'].capitalize(), i['name']))
        except KeyError:
            address_components = []

        for title in (address, postal_code, *address_components, point):
            if not title[1]:
                continue

            wiki_wiki = wikipediaapi.Wikipedia('en')
            p_wiki = wiki_wiki.page(title[1])

            if p_wiki.exists():
                links[title[0]] = (title[1], 'http://localhost:8080/wiki/' + title[1])
            else:
                links[title[0]] = (title[1], None)

    elif data['api'] == 'geosearch':
        organization = data['response']
        try:
            name = ('Name', organization['properties']['CompanyMetaData'].get('name'))
        except KeyError:
            name = ('Name', None)
        try:
            address = ('Address', organization['properties']['CompanyMetaData'].get('address'))
        except KeyError:
            address = ('Address', None)
        try:
            phone = ('Phone', organization['properties']['CompanyMetaData']['Phones'][0].get('formatted'))
        except KeyError:
            phone = ('Phone', None)
        try:
            hours = ('Hours', organization['properties']['CompanyMetaData']['Hours'].get('text'))
        except KeyError:
            hours = ('Hours', None)
        try:
            url = ('Url', organization['properties']['CompanyMetaData'].get('url'))
        except KeyError:
            url = ('Url', None)
        try:
            point = ('Point', '%f, %f' % tuple(organization['geometry']['coordinates']))
        except KeyError:
            point = ('Point', None)

        for title in (name, address, phone, hours, url, point):
            if not title[1]:
                continue

            wiki_wiki = wikipediaapi.Wikipedia('en')
            p_wiki = wiki_wiki.page(title[1])

            if p_wiki.exists():
                links[title[0]] = (title[1], 'http://localhost:8080/wiki/' + title[1])
            else:
                links[title[0]] = (title[1], None)

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
