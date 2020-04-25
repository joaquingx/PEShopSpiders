from flask import Flask, request
from similarity import hc_matrix, load_matrix
app = Flask(__name__)


@app.route("/")
def hello_world():
    input = request.args.get("input")
    threshold = request.args.get("threshold")
    return hc_matrix(input, threshold, index, tfidf, raw_corpus, dictionary, db)


if __name__ == '__main__':
    index, tfidf, raw_corpus, dictionary, db = load_matrix()
    app.run(host='127.0.0.1', port='5002')

