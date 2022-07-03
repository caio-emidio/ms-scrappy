#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import bs4
import flask

from flask import Flask
from flask import jsonify
from flask import request
import random
# apps
import services.investments.source as investments
import services.filmes.source as filmes
import services.futebol.source as futebol

app = Flask(__name__)


@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return jsonify({"data": random.random()})


@app.route('/investments/now', methods=['POST'])
def investmentNow():
    if request.method == 'POST':
        body = request.json
        return jsonify(investments.listAcoes(body['acoes']))


@app.route('/filmes', methods=['POST'])
def filmesagora():
    body = request.json
    return jsonify(filmes.result(body['url']))


@app.route('/filmes/detalhes', methods=['POST'])
def detalhesfilmes():
    body = request.json
    return jsonify(filmes.detalhes_filme(body['url']))


@app.route('/futebol/resultados', methods=['GET'])
def resultados():
    return jsonify(futebol.busca("resultados"))


@app.route('/futebol/calendario', methods=['GET'])
def calendario():
    return jsonify(futebol.busca("calendario"))


if __name__ == '__main__':
    app.run(debug=True)
