# project/main/views.py

# Api KEY: 7FOHNX2L98IZ


from flask import render_template, Blueprint, redirect, url_for, jsonify
from .forms import SearchForm
import requests
import json
import urllib.request,urllib.parse,urllib.error
import pprint

# set the apikey and limit
apikey = "7FOHNX2L98IZ"  # test value
lmt = 8

# load the user's anonymous ID from cookies or some other disk storage
# anon_id = <from db/cookies>

# ELSE - first time user, grab and store their the anonymous ID
r = requests.get("https://api.tenor.com/v1/anonid?key=%s" % apikey)

if r.status_code == 200:
    anon_id = json.loads(r.content)["anon_id"]
    # store in db/cookies for re-use later
else:
    anon_id = ""

# our test search
search_term = "CodeDoor"

# get the top 8 GIFs for the search term
r = requests.get(
    "https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s&anon_id=%s" %   
     (search_term, apikey, lmt, anon_id))

if r.status_code == 200:
    # load the GIFs using the urls for the smaller GIF sizes
    pp = pprint.PrettyPrinter(indent=4)
    gifs_result = json.loads(r.content)
    # pp.pprint(top_8gifs['results']) #pretty prints the json file.

    # for i in range(len(top_8gifs['results'])):
        # url = top_8gifs['results'][i]['media'][0]['gif']['url'] #This is the url from json.
        # print (url)
        # urllib.request.urlretrieve(url, str(i)+'.gif') #Downloads the gif file.
else:
    gifs_result = None

main_blueprint = Blueprint('main', __name__,)


@main_blueprint.route('/', methods=('GET', 'POST'))
def search():
    form = SearchForm()
    if form.validate_on_submit():
        return search_results(form.searchterm.data)

    return render_template('main/index.html', form=form)


@main_blueprint.route("/results")
def search_results(search_query):
    return render_template('main/results.html', results=gifs_result,
                           query=search_query)


def query_API(searchterm):
    tenor_apikey = None
    return tenor_apikey

