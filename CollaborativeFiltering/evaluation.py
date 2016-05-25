import math

def compute_rmse(prediction_dict):
	sum_of_squared = 0
	count = 0
	for user in prediction_dict:
		restaurants = prediction_dict[user]
		for r in restaurants:
			sum_of_squared += math.pow(restaurants[r][0] - restaurants[r][1],2)
			count += 1

	rmse = math.sqrt(sum_of_squared / count)
	return rmse
