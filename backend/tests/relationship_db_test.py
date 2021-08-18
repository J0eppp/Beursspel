from unittest import TestCase, main
from database import database

class TestDBRelationship(TestCase):
	def test_User_Player(self):
		# session = database.Session()

		# user = database.User(user_name="Joop")
		# database.add_user(session, user)

		# player = database.Player(player_money=1000, player_ready=False)
		# session.add(player)
		# session.commit()

		# session.refresh(player)
		# session.expunge(player)

		# user.player_id = player.player_id
		# session.merge(user)
		# session.commit()

		# print(user.player_id)
		# session.close()

		print(database.print_db())




if __name__ == '__main__':
	main()