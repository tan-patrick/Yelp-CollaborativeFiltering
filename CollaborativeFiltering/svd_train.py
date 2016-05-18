from numpy import *

class Residual:
	def __init__(self, value, current_error, previous_error):
		self.value = value
		self.current_error = current_error
		self. previous_error = previous_error

class Rating_Set:
	def __init__(self, value, current_error, previous_error):
		self.value = value

class Ratings_Model:
	def __init__(self, user_to_index, item_to_index, U, S, V):
		self.user_to_index = user_to_index
		self.item_to_index = item_to_index
		self.U = U
		self.S = S
		self.V = V

def train(rating_set, max_rank, min_epochs=0, max_epochs=100, learning_rate=0.001):
	user_features = [0.1 for i in range(rating_set.users_map)]
	item_features = [0.1 for i in range(rating_set.items_map)]
	residuals = [Residual(rating.value, 0.0, 0.0) for rating in rating_set.training_set]
	num_ratings = len(rating_set.training_set)
	for rank in range(1, max_rank):
		errors = [0.0, Inf, Inf]
		for i in range(1, max_epochs):
			for j in range(1, num_ratings):
				rating, residual = rating_set.training_set[j], residuals[j]
				item_feature = item_features[rating.item, rank]
				user_feature = user_features[rating.user, rank]
				residual.curr_error = residual.value - user_feature * item_feature
				error_diff = residual.prev_error - residual.curr_error
				errors[1] += error_diff * error_diff
				residual.prev_error = residual.curr_error
				item_features[rating.item, rank] += learning_rate * (residual.curr_error * user_feature - regularizer * item_feature)
				user_features[rating.user, rank] += learning_rate * (residual.curr_error * item_feature - regularizer * user_feature)
			if i > min_epochs and errors[1] < errors[2] and errors[2] > errors[3]:
				break
			errors[1], errors[2], errors[3] = 0.0, errors[1], errors[2]
		for residual in residuals:
			residual.value = residual.curr_error
			residual.prev_error = 0.0
	singular_values = [norm(user_features[:,rank]) * norm(item_features[:,rank]) for rank in range(1,max_rank)]
	for rank in range(1,max_rank):
		user_features[:,rank] /= norm(user_features[:,rank])
		item_features[:,rank] /= norm(item_features[:,rank])
	return Ratings_Model(rating_set.user_to_index,
                        rating_set.item_to_index,
                        user_features,
                        singular_values,
                        item_features)

if __name__ == "__main__":
	#load data, and then call train function
	