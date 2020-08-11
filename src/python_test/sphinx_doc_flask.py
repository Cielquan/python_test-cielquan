"""Serve sphinx docs."""
from flask import Flask


app = Flask(__name__)


@app.route("/docs/", defaults={"filename": "index.html"})
@app.route("/docs/<path:filename>")
def web_docs(filename):
    """Route the given doc page.

    :param filename: File name from URL
    :return: Doc page
    """
    app.static_folder = "static/docs"
    rv = app.send_static_file(filename)
    app.static_folder = "static"
    return rv


if __name__ == "__main__":
    app.run(debug=True)  # nosec
