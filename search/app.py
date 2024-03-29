""" Module for web api with property search endpoints. """

import flask

from . import main as core

app = flask.Flask(__name__)


@app.route("/")
def welcome():
    """Function on '/' printing welcome message."""
    return "Welcome to webscrappe-trademe-co-nz-property!"


@app.route("/search-without-detail")
@app.route("/search-without-detail/<city>/<int:total_pages>", methods=["GET"])
def search_without_detail(city=core.DEFAULT_CITY, total_pages=1):
    """Function on 'search-without-detail/<city>/<total_pages' searching
    without property detail."""
    result = core.search_without_detail(city=city, total_pages=total_pages)
    return _make_response(result)


@app.route("/search-with-detail")
@app.route("/search-with-detail/<city>/<int:total_pages>", methods=["GET"])
def search_with_detail(city=core.DEFAULT_CITY, total_pages=1):
    """Function on '/search-with-detail/<city>/<total_pages>' searching
    with property detail."""
    result = core.search_with_detail(city=city, total_pages=total_pages)
    return _make_response(result)


def _make_response(result):
    csv = core.format_psv(result)
    response = None
    if csv:
        response = flask.make_response(csv, 200)
        response.mimetype = "text/plain"
    else:
        response = flask.make_response("", 204)
    return response


def main():
    """Entry point if called as an executable."""
    app.run(host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
