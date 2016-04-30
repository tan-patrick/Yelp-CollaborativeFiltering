# User and Users classes for user data
import json

class User(object):

	# json_obj = user's json object from user data file
	def __init__(self, json_obj):
		self.user = json.loads(json_obj)
		self.reviews = dict() # key=restaurant, value=review text
		#self.topics = not sure yet what type of data structure

	def user_id(self):
		return self.user['user_id']
		
	def name(self):
		return self.user['name']

	def review_count(self):
		return self.user['review_count']

	def average_stars(self):
		return self.user['average_stars']

	def votes(self):
		return self.user['votes']

	def friends(self):
		return self.user['friends']

	def elite(self):
		return self.user['elite']

	def compliments(self):
		return self.user['compliments']

	def fans(self):
		return self.user['fans']

	def reviews(self):
		return self.reviews

	def add_review(self, review):
		rid = review['business_id']
		self.reviews[rid] = review['text']

	# load all user's reviews into User
	def load_reviews(self, reviews_data_file):
		uid = self.user_id()
		
		with open(reviews_data_file, 'r') as rf:
			for entry in rf:
				review = json.loads(entry)	
				if uid == review['user_id']:
					self.add_review(review)

	# topic-term matrix from LDA
	#def load_topics(self, topics):
			

class Users(object):

	def __init__(self, user_data_file):
		self.users = list()
		self.load_users(user_data_file)

	def add(self, user):
		self.users.append(user)

	def list_users(self):
		return self.users

	# load all users into Users class from user_data_file	
	def load_users(self, user_data_file):
		with open(user_data_file, 'r') as uf:
			for entry in uf:
				user = User(entry)
				self.add(user)
