# project/main/views.py
from flask import render_template, Blueprint, redirect, url_for, jsonify
from .forms import SearchForm
import requests
import json

main_blueprint = Blueprint('main', __name__,)


@main_blueprint.route('/', methods=('GET', 'POST'))
def search():
    form = SearchForm()
    if form.validate_on_submit():
        return search_results(form.searchterm.data)

    return render_template('main/index.html', form=form)


@main_blueprint.route("/results")
def search_results(search_query):
    return render_template('main/results.html', results=query_API(search_query),
                           query=search_query)


def query_API(searchterm):
    tenor_apikey = "7FOHNX2L98IZ"

    # specify the anonymous_id tied to the given user
    # load the user's anonymous ID from cookies or some other disk storage
    # anon_id = <from db/cookies>
    # ELSE - first time user, grab and store their the anonymous ID
    r = requests.get("https://api.tenor.com/v1/anonid?key=%s" % tenor_apikey)

    if r.status_code == 200:
        anon_id = json.loads(r.content)["anon_id"]
        # store in db/cookies for re-use later
    else:
        anon_id = ""

    # get the GIFs for the search term
    r = requests.get(
        "https://api.tenor.com/v1/search?q=%s&key=%s&anon_id=%s" %
        (searchterm, tenor_apikey, anon_id))

    if r.status_code == 200:
        # load the GIFs using the urls for the smaller GIF sizes
        gifs_result = json.loads(r.content)
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(gifs_result) #pretty prints the json file.
    else:
        gifs_result = None

    return gifs_result
