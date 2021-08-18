from types import resolve_bases
from flask import jsonify, request, Response, g
import json
from .middleware import login_required

# Import the BluePrint from the main file
from . import main
v1bp = main.v1bp

from database import database

@v1bp.route("/users", methods=["GET"])
@login_required
def users_get():
	params = request.args
	username = params.get("username")
	session = database.Session()
	if username == None:
		res = jsonify([item.serialize for item in database.get_users(session)])
		session.close()
		return res

	res = jsonify(database.get_user_by_username(session, username).serialize)
	session.close()
	return res
		
# User registration
@v1bp.route("/users", methods=["POST"])
def users_post():
	username = request.json.get("username")
	password = request.json.get("password")
	
	if username is None or password is None:
		return jsonify({ "error": "you did not specify a username/password" }), 400
	
	session = database.Session()
	# Check if the user exists
	if database.get_user_by_username(session, username).user_name is not None:
		session.close()
		return jsonify({ "error": "a user with this username already exists" }), 400
	
	# Everything is fine, create the user
	user = database.User(user_name=username)
	user.hash_password(password)
	database.add_user(session, user)
	session.close()
	return jsonify(user.serialize), 201

@v1bp.route("/me", methods=["GET"])
@login_required
def me_get():
	return jsonify(g.user.serialize)

@v1bp.route("/session", methods=["POST"])
def session_post():
	try:
		print(request.json)
		username = request.json.get("username")
		password = request.json.get("password")

		if username is None or password is None:
			return jsonify({ "error": "please provide a username and password" }), 400
	
		# Get the user from the database
		session = database.Session()
		user = database.get_user_by_username(session, username)
		if user.verify_password(password) == False:
			# Wrong password
			session.close()
			return jsonify({ "error": "wrong password" }), 401

		# Password is correct, generate a token
		token = str(user.generate_auth_token(), encoding="utf-8")
		
		res = Response()
		res.headers["Authentication"] = token
		res.set_data(json.dumps({ "token": token }))
		session.close()
		return res, 201

	except Exception as e:
		e = str(e)
		status = 500
		if "Bad Request" in e:
			status = 400

		return jsonify({ "error": e }), status

@v1bp.route("/session", methods=["GET"])
@login_required
def session_get():
	return jsonify({ "token": g.user.token }), 200