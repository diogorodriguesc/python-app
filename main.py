from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World!"


if __name__ == "__main__":
    from container import Container
    import os

    try:
        container = Container(os.getenv("SITEMAPS_INDEXING_ENVIRONMENT"))
    except Exception as exception:
        print(exception)

    app.run(debug=True)
