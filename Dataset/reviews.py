# Reviews class for reviews data
import json

class Reviews(object):
	
	def __init__(self, reviews_file):
		# maps user_id's to their reviews
		self.reviews = dict() # { user_id => { business_id => revivew_text } }
		self.load_reviews(reviews_file)

	# load reviews from reviews.json file
	def load_reviews(self, reviews_file):
		count = 1;
		with open(reviews_file, 'r') as rf:
			for entry in rf:
				print("Loading from file: %d of 1363242" % count)
				count = count + 1
				review = json.loads(entry)
				user_id = review['user_id']
				restaurant = review['business_id']
				if user_id not in self.reviews:
					self.reviews[user_id] = dict()
				self.reviews[user_id][restaurant] = review['text']

	# return dictionary of business_id => review_text for each of
	# the restaurants reviewed by uid
	def get_reviews_for_user(self, uid):
		try:
			return self.reviews[uid]
		except KeyError:
			return None
