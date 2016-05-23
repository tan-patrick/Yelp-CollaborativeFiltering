from numpy import *
from load_dataset import *
from classes import Residual, RatingSet, RatingsModel, Rating

def train(rating_set, max_rank, min_epochs=0, max_epochs=100, learning_rate=0.001, regularizer=0.02):
	user_features = full((len(rating_set.user_to_index), max_rank), 0.1)
	item_features = full((len(rating_set.item_to_index), max_rank), 0.1)
	# print item_features.shape
	residuals = [Residual(rating.value, 0.0, 0.0) for rating in rating_set.training_set]
	num_ratings = len(rating_set.training_set)
	# print num_ratings
	for rank in range(max_rank):
		errors = [0.0, Inf, Inf]
		for i in range(max_epochs):
			for j in range(num_ratings):
				rating, residual = rating_set.training_set[j], residuals[j]
				# print rating.item, rank
				item_feature = item_features[rating.item, rank]
				user_feature = user_features[rating.user, rank]
				residual.curr_error = residual.value - user_feature * item_feature
				error_diff = residual.previous_error - residual.curr_error
				errors[0] += error_diff * error_diff
				residual.prev_error = residual.curr_error
				item_features[rating.item, rank] += learning_rate * (residual.curr_error * user_feature - regularizer * item_feature)
				user_features[rating.user, rank] += learning_rate * (residual.curr_error * item_feature - regularizer * user_feature)
			if i > min_epochs and errors[0] < errors[1] and errors[1] > errors[2]:
				break
			errors[0], errors[1], errors[2] = 0.0, errors[0], errors[1]
		for residual in residuals:
			residual.value = residual.curr_error
			residual.prev_error = 0.0
	singular_values = [linalg.norm(user_features[:,rank]) * linalg.norm(item_features[:,rank]) for rank in range(max_rank)]
	for rank in range(max_rank):
		user_features[:,rank] /= linalg.norm(user_features[:,rank])
		item_features[:,rank] /= linalg.norm(item_features[:,rank])
	return RatingsModel(rating_set.user_to_index,
                        rating_set.item_to_index,
                        user_features,
                        singular_values,
                        item_features)

if __name__ == "__main__":
	rating_set = load_dataset()
	model = train(rating_set, 1, 0, 1)

