import sqlalchemy as sa
import os

from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker

from passlib.apps import custom_app_context as pwd_context
from bcrypt import gensalt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from dotenv import load_dotenv

load_dotenv()


database_uri = os.getenv("DATABASE_URI")
print(database_uri)
engine = sa.create_engine(database_uri)
SQLAlchemyBase = declarative_base()
Session = sessionmaker(bind=engine)

SECRET_KEY = os.getenv("SECRET_KEY")

# Database schemas
class User(SQLAlchemyBase):
	__tablename__ = "users"
	user_id = sa.Column(sa.Integer, primary_key=True)
	user_name = sa.Column(sa.String(55))
	user_hash = sa.Column(sa.String(128))
	user_salt = sa.Column(sa.String(32))


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