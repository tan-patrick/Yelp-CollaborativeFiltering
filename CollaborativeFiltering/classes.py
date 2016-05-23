class Residual:
	def __init__(self, value, current_error, previous_error):
		self.value = value
		self.current_error = current_error
		self.previous_error = previous_error

class Rating:
	def __init__(self, user, item, value):
		self.user = user
		self.item = item
		self.value = value

class RatingSet:
	def __init__(self, training_set, test_set, user_to_index, item_to_index):
		self.training_set = training_set
		self.test_set = test_set
		self.user_to_index = user_to_index
		self.item_to_index = item_to_index

class RatingsModel:
	def __init__(self, user_to_index, item_to_index, U, S, V):
		self.user_to_index = user_to_index
		self.item_to_index = item_to_index
		self.U = U
		self.S = S
		self.V = V