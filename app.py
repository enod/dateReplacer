# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import urllib2
from bs4 import BeautifulSoup
from dater import mapping_replace

app = Flask(__name__)

@app.route('/', methods=['POST'])
def poster():
    """
    Receives POST request with a link from a client.
    Parses html page and send texts from page to dater for further analysis.
    :return: text that all dates are replaced by ISO 8601 format.
    """
    url = request.json['url']
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page,"html.parser")

    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return mapping_replace(text)


@app.route('/', methods=['GET'])
def getter():
    return jsonify({"message": 'It works!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
