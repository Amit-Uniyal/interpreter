import MySQLdb


class DB:
	def __init__(self):
		self.conn = MySQLdb.connect(
				host="localhost",
				port=3306,
				user="testuser",
				passwd="testpass",
				db="testflask"
		)

		self.c = self.conn.cursor()

	def run_query(self, query):
		self.c.execute(query)
		result = self.c.fetchall()

		return result

