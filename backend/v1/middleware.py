from functools import wraps
from flask import g, request, jsonify, Response
import json

from database import database

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		token = request.headers.get("Authentication")
		if token == None:
			return jsonify({ "error": "the Authentication header is missing" }), 401
		session = database.Session()
		user = database.User.verify_auth_token(session, token)
		if user == None:
			return jsonify({ "error": "invalid token" }), 401

		g.user = user

		# Renew token
		token = str(user.generate_auth_token(), encoding="utf-8")
		
		res = Response()
		res.headers["Authentication"] = token
		res.set_data(json.dumps({ "token": token }))
		session.close()
		return f(*args, **kwargs)
	return decorated_function