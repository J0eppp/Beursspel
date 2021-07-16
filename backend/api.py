#!/usr/bin/python3
import flask
from flask import request, jsonify, g
# must be imported for initialization of database.
from database import database
import os

from v1.main import v1bp


app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Setup routes
app.register_blueprint(v1bp, url_prefix="/api/v1/")

# Setup ACAO headers (CORS)
@app.after_request
def after_request(response):
	header = response.headers
	# header['Access-Control-Allow-Origin'] = 'http://localhost:3000'
	header['Access-Control-Allow-Origin'] = 'https://beursspel.j0eppp.dev'

	header['Access-Control-Allow-Headers'] = "Authentication, Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"
	# header['Access-Control-Allow-Credentials'] = "true"
	if g.get("user") is not None and g.user.token is not None:
		header["Authentication"] = g.user.token

	response.headers = header
	return response

# Run flask
app.run(port=5004)
