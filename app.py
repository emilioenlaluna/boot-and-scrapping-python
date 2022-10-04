import datetime
import json
import urllib
from urllib.parse import quote_plus

import feedparser
import requests
from flask import Flask
from flask import make_response
from flask import render_template
from flask import request

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'nyt': 'https://rss.nytimes.com/services/xml/rss/nyt/World.xml',
             'fox': 'https://moxie.foxnews.com/feedburner/latest.xml',
             'yahoo': 'https://www.yahoo.com/news/rss',
             'other': 'https://feeds.simplecast.com/54nAGcIl'
             }

DEFAULTS = {'publication': 'bbc',
            'city': 'Aguascalientes, MX',
            'currency_from': 'GBP',
            'currency_to': 'USD'}


@app.route('/', methods=['GET', 'POST'])
@app.route("/")
def home():
    publication = get_value_with_fallback("publication")
    articles = get_news(publication)

    city = get_value_with_fallback("city")
    weather = get_weather(city)

    currency_from = get_value_with_fallback("currency_from")
    currency_to = get_value_with_fallback("currency_to")
    rate, currencies = get_rates(currency_from, currency_to)

    response = make_response(render_template("home.html",
                                             articles=articles,
                                             weather=weather, currency_from=currency_from,
                                             currency_to=currency_to, rate=rate,
                                             currencies=sorted(currencies)))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("publication", publication,
                        expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from",
                        currency_from, expires=expires)
    response.set_cookie("currency_to",
                        currency_to, expires=expires)
    return response


def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']


def get_weather(query):
    api_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=5870b9af49936431c5939ac54c943f0d'
    query = urllib.parse.quote(query)
    url = api_url.format(query)
    data = urllib.request.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description":
                       parsed["weather"][0]["description"],
                   "temperature": parsed["main"]["temp"],
                   "city": parsed["name"],
                   'country': parsed['sys']['country']
                   }
    return weather


def get_rates(frm, to):
    api_url = 'http://api.exchangeratesapi.io/v1/latest?access_key=739d9192231ed16df0e2c4c7738043c2&format=1'
    all_currency = urllib.request.urlopen(api_url).read()
    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return (to_rate / frm_rate, parsed.keys())


def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)

    return DEFAULTS[key]


@app.route('/boot', methods=['GET', 'POST'])
def boot():
    # Se guarda en "respuesta", el resultado de hacer la petición GET:
    respuesta = requests.get("https://api.thecatapi.com/v1/images/search")
    print(respuesta)  # ---> Imprime algo como <Response[200]>;

    # Para obtener los meta-datos que trae la petición:
    estatus = respuesta.status_code
    cabezera = respuesta.headers
    contenido = respuesta.content
    texto = respuesta.text
    contenidox = respuesta._content
    encoding = respuesta.encoding

    # Se convierte la respuesta a un archivo JSON para procesarlo:
    respuestaEnJSON = respuesta.json()
    print(respuestaEnJSON)  # ---> Imprime el JSON de la respuesta>;

    # SI QUERÉMOS SÓLO EL CONTENIDO DE LA RESPUESTA:
    contenidoRespuesta = respuesta.content

    # SI EL CONTENIDO DE LA RESPUESTA ES CÓDIGO HTML;
    # ES NECESARIO DECODIFICARLO PARA EVITAR ERRORES CON CARACTERES ESPECIALES:
    contenidoRespuesta = respuesta.content.decode("utf-8")
    return render_template('api.html', respuesta=contenidoRespuesta, json=respuestaEnJSON, todaRespuesta=respuesta)


@app.route('/datosInutiles', methods=['GET', 'POST'])
def datosInutiles():
    # Se guarda en "respuesta", el resultado de hacer la petición GET:
    respuesta = requests.get("https://uselessfacts.jsph.pl/random.json")
    print(respuesta)  # ---> Imprime algo como <Response[200]>;

    # Para obtener los meta-datos que trae la petición:
    estatus = respuesta.status_code
    cabezera = respuesta.headers
    contenido = respuesta.content
    texto = respuesta.text
    contenidox = respuesta._content
    encoding = respuesta.encoding

    # Se convierte la respuesta a un archivo JSON para procesarlo:
    respuestaEnJSON = respuesta.json()
    print(respuestaEnJSON)  # ---> Imprime el JSON de la respuesta>;

    datoInutil = respuestaEnJSON["text"]

    # SI QUERÉMOS SÓLO EL CONTENIDO DE LA RESPUESTA:
    contenidoRespuesta = respuesta.content

    # SI EL CONTENIDO DE LA RESPUESTA ES CÓDIGO HTML;
    # ES NECESARIO DECODIFICARLO PARA EVITAR ERRORES CON CARACTERES ESPECIALES:
    contenidoRespuesta = respuesta.content.decode("utf-8")
    return render_template('datosInteresantes.html', data=datoInutil, respuesta=contenidoRespuesta,
                           json=respuestaEnJSON, todaRespuesta=respuesta)


@app.route('/pokeapi', methods=['GET', 'POST'])
def pokeapi():
    # Se guarda en "respuesta", el resultado de hacer la petición GET:
    respuesta = requests.get("https://pokeapi.co/api/v2/pokemon/ditto")
    print(respuesta)  # ---> Imprime algo como <Response[200]>;

    # Para obtener los meta-datos que trae la petición:
    estatus = respuesta.status_code
    cabezera = respuesta.headers
    contenido = respuesta.content
    texto = respuesta.text
    contenidox = respuesta._content
    encoding = respuesta.encoding

    # Se convierte la respuesta a un archivo JSON para procesarlo:
    respuestaEnJSON = respuesta.json()
    print(respuestaEnJSON)  # ---> Imprime el JSON de la respuesta>;

    # SI QUERÉMOS SÓLO EL CONTENIDO DE LA RESPUESTA:
    contenidoRespuesta = respuesta.content

    # SI EL CONTENIDO DE LA RESPUESTA ES CÓDIGO HTML;
    # ES NECESARIO DECODIFICARLO PARA EVITAR ERRORES CON CARACTERES ESPECIALES:
    contenidoRespuesta = respuesta.content.decode("utf-8")
    return render_template('datosInteresantes.html', respuesta=contenidoRespuesta, json=respuestaEnJSON,
                           todaRespuesta=respuesta)


@app.route('/gatito', methods=['GET', 'POST'])
def gatito():
    # Se guarda en "respuesta", el resultado de hacer la petición GET:
    respuesta = requests.get("https://api.thecatapi.com/v1/images/search")

    # Para obtener los meta-datos que trae la petición:
    estatus = respuesta.status_code
    cabezera = respuesta.headers
    contenido = respuesta.content
    texto = respuesta.text
    contenidox = respuesta._content
    encoding = respuesta.encoding

    # Se convierte la respuesta a un archivo JSON para procesarlo:
    respuestaEnJSON = respuesta.json()

    gato = respuestaEnJSON[0]["url"]
    return render_template('gatito.html', gato=gato)


@app.route('/gato', methods=['GET', 'POST'])
def gato():
    urlDeLaAPI = "https://api.thecatapi.com/v1/images/search"
    respuestaDelRequest = requests.get(url=urlDeLaAPI)
    print(respuestaDelRequest)

    '''
        ESCRIBIR "print(respuestaDelRequest." Y VER CÓMO VSCODE AUTO-
        COMPLETA Y TE DICE QUÉ ATRIBUTOS PUEDES OBTENER DE AHÍ.
    '''

    '''
        INTENTAR CON EL CÓDIGO SIGUIENTE PARA COMPROBAR LO DE ARRIBA:
        print("Status: " + respuestaDelRequest.status_code + "\n\n")
        DESPUÉS USAR EL SIGUIENTE CÓDIGO...
    '''

    print(f"Status: {respuestaDelRequest.status_code}\n")
    print(f"Content: {respuestaDelRequest.content}\n")
    print(f"Text: {respuestaDelRequest.text}\n")
    print(f"URL: {respuestaDelRequest.url}\n")
    print(f"Headers: {respuestaDelRequest.headers}\n")
    print(f"_Content: {respuestaDelRequest._content}\n")
    print(f"Encoding: {respuestaDelRequest.encoding}\n")

    # Obtener el link de la imagen de gatito #
    # Primero se necesita convertir a un JSON #
    # * print("\n\n", respuestaDelRequest.json())
    respuestaEnJSON = respuestaDelRequest.json()
    print(respuestaEnJSON)

    '''
        El JSON luce así...
        * Los corchetes indican que es un vector...
        * Cuando se quiere acceder al elemento de un vector, se usan
          corchetes con un número, para indicar cuál elemento...
        [
            * Las llaves indican que es un objeto...
            * Cuando se quiere acceder al valor de un atributo, se
              coloca ["nombreDelAtributo"]...
            {
                "nombreDelAtrbuto": "valorDelAtributo"
            }
        ]
    '''

    # Queremos obtener el atributo "url", para saber dónde está
    # la foto del gato, y este atributo está en el [0]["url"]...
    '''
        Elemento [0]...
        [
            Atributo ["url"]...
            {
                "id": "MTcyNTg3OA",
                "url": "https://cdn2.thecatapi.com/images/MTcyNTg3OA.png",
                "width": 160,
                "height": 160
            }
        ]
    '''
    urlFotoGatito = respuestaEnJSON[0]["url"]
    print(urlFotoGatito)

    # Se usa una librería para abrir la foto del gatito #
    # Esta librería ya está incluída dentro de Python 3 #
    import webbrowser
    webbrowser.open(urlFotoGatito)
    return 'ventana abierta'


import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


@app.route('/spotify', methods=['GET', 'POST'])
def spotify():
    # ! IMPORTANTE LEER https://developer.spotify.com/documentation/web-api/ #
    # Para rolas de Led Zeppelin #
    # ? Para obtener el URI de un artista...
    # ? IR AL PERFIL DEL ARTISTA, COPIAR EL URL Y SEPARAR...
    # / https://open.spotify.com/artist/     36QJpDe2go2KgaRleHCDTp
    # * URI = "spotify:artist:<colocar lo separado en el link>" #
    uriLedZeppelin = "spotify:artist:36QJpDe2go2KgaRleHCDTp"

    # Credenciales #
    # TODO: --------------------------------------------------
    # ! ESCONDER ESTAS CREDENCIALES EN UN ARCHIVO NO LEGIBLE #
    CLIENT_ID = "394c850b632e4d14babe4548aa1415a4"
    CLIENT_SECRET = "50145021c9af48c889fc2398c119b840"

    # ? Crea la conexión a la API y trae los resultados de una petición #
    spotify = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))
    results = spotify.artist_top_tracks(uriLedZeppelin)

    # * Estructura para guardar info del top de Led Zeppelin #
    names = []
    tracks = []
    covers = []

    print()
    # / Lee los tracks y guarda los datos #
    for track in results["tracks"][:10]:
        print("Canción : " + track["name"])
        print("Audio   : " + track["preview_url"])
        print("Portada : " + track["album"]["images"][0]["url"])
        print()

        # names.append(track["name"])
        # tracks.append(tracks["preview_url"])
        # covers.append(track["album"]["images"][0]["url"])

    # Imprime los álbums #
    # for song in range(0, 10):
    #     print("Canción : " + names[song])
    #     print("Audio   : " + tracks[song])
    #     print("Portada : " + covers[song])
    #     print()
    return results



@app.route('/PokeAPI', methods=['GET', 'POST'])
def PokeAPI():
    # envía una solicitud GET al URL especificado
    pokemonResponse = requests.get("https://pokeapi.co/api/v2/pokemon/" + "pikachu")

    # en base a los códigos de estatus, se hace un IF, si resulta correcto
    # hace lo que se le indica
    if pokemonResponse.status_code == 200:
        pokemonResponse_JSON = pokemonResponse.json()
        especie = pokemonResponse_JSON["species"]["name"]
        altura = pokemonResponse_JSON["height"]
        peso = pokemonResponse_JSON["weight"]
        sprite = pokemonResponse_JSON["sprites"]["other"]["dream_world"]["front_default"]
        # messagebox.showinfo(message= "Nombre: " + especie + "\n Altura: " + altura + "\nPeso: " + weight)
        # print("Nombre: ", especie, "\n")
        # print("Altura: ", height," \n ")
        # print("Peso: ", weight, " \n ")
        print(especie, altura, peso, sprite)
    return 'zzz'

from lyricsgenius import Genius
@app.route('/licrs', methods=['GET', 'POST'])
def licrs():
    '''
        LEYENDO https://docs.genius.com/#/songs-h2 SE DESCUBRE QUE
        PARA OBTENEY EL LYRICS DE UNA CANCIÓN, PRIMERO HAY QUE SABER
        EL ID DE LA CANCIÓN ... AAAAAAAAAAH!!!
    '''

    #! http://api.genius.com/search?q={search_term}&access_token={client_access_token} #

    genius = Genius("kePhLRukAjzj2ELECp4zAh9Nc-4HzE002017OEXRTK47E8ZfkSszT_n2LVRYMVal")
    genius.search_artist('Andy Shauf')
    print(genius)


#hola mundo

if __name__ == '__main__':
    app.run()
