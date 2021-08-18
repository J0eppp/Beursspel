import sqlalchemy as sa
import os
from enum import Enum

from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker, relationship

from passlib.apps import custom_app_context as pwd_context
from bcrypt import gensalt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from dotenv import load_dotenv

from datetime import datetime

load_dotenv()


database_uri = os.getenv("DATABASE_URI")
engine = sa.create_engine(database_uri)
SQLAlchemyBase = declarative_base()
Session = sessionmaker(bind=engine)

SECRET_KEY = os.getenv("SECRET_KEY")


class CompanyType(Enum):
	BV = 1
	NV = 2
	VOF = 3

# Database schemas
class Company(SQLAlchemyBase):
	__tablename__ = "companies"
	company_id = sa.Column(sa.Integer(), primary_key=True)
	game_id = sa.Column("game_id", sa.Integer(), sa.ForeignKey("games.game_id"))
	company_start_value = sa.Column(sa.Float()) # 20-80
	company_value = sa.Column(sa.Float())
	company_amount = sa.Column(sa.Float()) # 375
	company_volatility = sa.Column(sa.Float()) # >0 and <= 1
	company_type = sa.Column(sa.Enum(CompanyType))

class Stock(SQLAlchemyBase):
	__tablename__ = "stocks"
	stock_id = sa.Column(sa.Integer(), primary_key=True)
	game_id = sa.Column("game_id", sa.Integer(), sa.ForeignKey("games.game_id"))
	company_id = sa.Column("company_id", sa.Integer(), sa.ForeignKey("companies.company_id"))
	player_id = sa.Column("player_id", sa.Integer(), sa.ForeignKey("players.player_id"))
	stock_amount = sa.Column(sa.Integer())
	stock_value_bought = sa.Column(sa.Float())

class Round(SQLAlchemyBase):
	__tablename__ = "rounds"
	round_id = sa.Column(sa.Integer(), primary_key=True)
	game_id = sa.Column("game_id", sa.Integer(), sa.ForeignKey("games.game_id"))
	round_round = sa.Column(sa.Integer())
	round_time_started = sa.Column(sa.Time())
	round_total_player_money = sa.Column(sa.Float())
	round_total_player_stocks_value = sa.Column(sa.Float())
	# game = relationship("Game")

	@property
	def serialize(self):
		return {
			"id": self.round_id,
			"round": self.round_round,
			"time_started": self.round_time_started.strftime("%H:%M:%S"),
			"total_player_money": self.round_total_player_money,
			"total_player_stocks_value": self.round_total_player_stocks_value,
		}

class Game(SQLAlchemyBase):
	__tablename__ = "games"
	game_id = sa.Column(sa.Integer(), primary_key=True)
	game_round_number = sa.Column(sa.Integer())

	game_round = relationship("Round")

	def total_player_money(self):
		return 0

	def total_player_stocks_value(self):
		return 0	

	def new_round(self):
		new_round = Round(game_id=self.game_id, round_round=self.game_round_number + 1, round_time_started=datetime.now(), round_total_player_money=self.total_player_money(), round_total_player_stocks_value=self.total_player_stocks_value())
		session = Session()
		session.add(new_round)
		session.commit()
		Game.game_round = new_round

		session.refresh(new_round)
		session.expunge(new_round)

		session.close()

	@property
	def serialize(self):
		return {
			"id": self.game_id,
			"round": self.game_round.serialize,
		}


class Player(SQLAlchemyBase):
	__tablename__ = "players"
	player_id = sa.Column(sa.Integer(), primary_key=True)
	game_id = sa.Column("game_id", sa.Integer(), sa.ForeignKey("games.game_id"))
	player_money = sa.Column("player_money", sa.Float())
	player_ready = sa.Column(sa.Boolean()) # Can we continue to the next round?

	user = relationship("User")

	@property
	def serialize(self):
		return {
			"id": self.player_id,
			"game_id": self.game_id,
			"money": self.player_money,
			"ready": self.player_ready
		}





class User(SQLAlchemyBase):
	__tablename__ = "users"
	user_id = sa.Column("user_id", sa.Integer(), primary_key=True)
	user_name = sa.Column(sa.String(55))
	user_hash = sa.Column(sa.String(128))
	user_salt = sa.Column(sa.String(32))

	player_id = sa.Column(sa.Integer(), sa.ForeignKey("players.player_id"))

	token = None


	def hash_password(self, password):
		# TODO generate salt
		salt = str(gensalt())
		self.user_salt = salt
		self.user_hash = pwd_context.encrypt(password + salt)

	def verify_password(self, password) -> bool:
		return pwd_context.verify(password + self.user_salt, self.user_hash)

	def generate_auth_token(self, expiration = 3600):
		s = Serializer(SECRET_KEY, expires_in = expiration)
		token = s.dumps({ "id": self.user_id })
		self.token = str(token, encoding="utf-8")
		return token

	@staticmethod
	def verify_auth_token(session, token):
		s = Serializer(SECRET_KEY)
		try:
			data = s.loads(token)
		except SignatureExpired:
			return None # valid token, but expired
		except BadSignature:
			return None # invalid token
		return session.query(User).filter(User.user_id == data["id"]).first()

	@property
	def serialize(self):
		return {
			"id": self.user_id,
			"username": self.user_name,
		}

SQLAlchemyBase.metadata.create_all(engine)



# Game related stuff
def add_game(session, game):
	session.add(game)
	session.commit()

	session.refresh(game)
	session.expunge(game)


def get_games(session):
	return session.query(Game).filter().all()

def get_game_by_id(session, id):
	return session.query(Game).filter(Game.game_id == id).first()

def add_player(session, player):
	session.add(player)

	session.commit()

	session.refresh(player)
	session.expunge(player)

def get_player_by_user_id(session, id):
	return session.query(Player).filter(Player.user.user_id == id).first()



# User stuff
def get_user_by_username(session, username):
	user = session.query(User).filter(User.user_name == username).first()
	if user == None:
		return User() # User does ot exist
	return user
	
def add_user(session, user):
	session.add(user)
	session.commit()

	session.refresh(user)
	session.expunge(user)

def get_users(session):
	return session.query(User).filter().all()


def print_db():
	import pandas as pd

	return pd.read_sql_table(table_name="users", con=engine)