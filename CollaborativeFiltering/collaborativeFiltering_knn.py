import os
import sys
import json
import math
from time import time

path_to_Dataset = os.path.dirname(os.path.abspath(__file__))
path_to_Dataset = path_to_Dataset.replace("CollaborativeFiltering", "Dataset")
sys.path.append(path_to_Dataset)

import restaurants

# def compute_user_similarity(r1,r2):
# 	sum_diff = 0
# 	count = 0
# 	for r in r1:
# 		if r not in r2:
# 			continue
# 		sum_diff += math.pow(r1[r] - r2[r],2)
# 		count += 1
# 	sim_ui = float(sum_diff) / count
# 	return sim_ui

if __name__ == '__main__':
	start = time()
	restaurant_rating = {} #{restaurantid1:4.0,restaurantid2:3.5}
	user_average_rating = {} #{userid1:4.0,userid2:3.5...}
	baseline_prediction = {} #{userid1:{restaurant1:1.1, restaurant2:3.0,...}...}
	knn_prediction = {} #{userid1:{restaurant1:1.1, restaurant2:3.0,...}...}
	restaurant_index = {} #{restaurant1: {user1: 4.0,..}}
	user_index = {} #{userid1:{restaurant1:1.1, restaurant2:3.0,...}...}

	# compute the average rating of all restaurants by all users -> average_restaurants_rating
	restaurant_data_path = "/restaurants.json"
	restaurants = restaurants.Restaurants(path_to_Dataset + restaurant_data_path)
	sum_restaurants_rating = 0
	for restaurant in restaurants.list_restaurants():
		restaurant_id = restaurant.business_id()
		rating = restaurant.stars()

		# construct restaurant_rating dictionary 
		restaurant_rating[restaurant_id] = rating

		sum_restaurants_rating += rating
	average_restaurants_rating = float(sum_restaurants_rating) / len(restaurants.list_restaurants())
	
	print average_restaurants_rating # 3.48211080531
	print "Time after computing average rating for all: %d s" % (time() - start)
	# loop through all the reviews, compute the bias between [average_restaurants_rating, user's average rating] & [average_restaurants_rating, restaurant's average rating]
	# construct user_average_rating dictionary 
	user_data_path = "/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_user.json"
	with open(user_data_path, 'r') as uf:
		for entry in uf:
			user = json.loads(entry)
			user_id = user['user_id']
			average_rating = user['average_stars']
			user_average_rating[user_id] = average_rating
	print "Time after constructing user rating index: %d s" % (time() - start)

	# compute baseline prediction rating as predicted_rating = average_restaurants_rating + bias_user + bias_restaurant
	review_data_path = "/reviews.json"
	with open(path_to_Dataset + review_data_path, 'r') as rf:
		for entry in rf:
			review = json.loads(entry)
			review_user_id = review['user_id']
			review_restaurant_id = review['business_id']
			review_user_average_rating = user_average_rating[review_user_id]
			review_restaurant_rating = restaurant_rating[review_restaurant_id]	
			predicted_rating = average_restaurants_rating + (review_user_average_rating-average_restaurants_rating) + (review_restaurant_rating-average_restaurants_rating)
			if review_user_id not in baseline_prediction:
				baseline_prediction[review_user_id] = {review_restaurant_id: predicted_rating}
			else:
				baseline_prediction[review_user_id][review_restaurant_id] = predicted_rating

			# construct restaurant index for later use
			review_rating = review['stars']
			if review_restaurant_id not in restaurant_index:
				restaurant_index[review_restaurant_id] = {review_user_id: review_rating}
			else:
				restaurant_index[review_restaurant_id][review_user_id] = review_rating

			# construct user index for later use
			if review_user_id not in user_index:
				user_index[review_user_id] = {review_restaurant_id: review_rating}
			else:
				user_index[review_user_id][review_restaurant_id] = review_rating

	# print restaurant_index['zMN8UGd1zDEreT58OCdnyg']['18kPq7GPye-YQ3LyKyAZPw']
	# print baseline_prediction['18kPq7GPye-YQ3LyKyAZPw']
	print "Time after baseline prediction: %d s" % (time() - start)


	# predict how user u would rate on restaurant r by knn
	# find N nearest users who has rated r
	# r_predict = baseline_ur + all N users as user i sum(r_ir - baseline_ir ) * similarity(ui)
	N = 5
	temp_sim = 0.3
	with open(path_to_Dataset + review_data_path, 'r') as rf:
		for entry in rf:
			review = json.loads(entry)
			review_user_id = review['user_id']
			review_restaurant_id = review['business_id']
			baseline_ur = baseline_prediction[review_user_id][review_restaurant_id]

			# users that rated this restaurant
			review_users = restaurant_index[review_restaurant_id]

			# compute similarity -- naive knn
			# user_similarity_index = {}
			# for user in review_users:
			# 	reviewed_by_user_u = user_index[review_user_id]
			# 	reviewed_by_user_i = user_index[user]
			# 	sim_ui = compute_user_similarity(reviewed_by_user_u,reviewed_by_user_i)
			# 	user_similarity_index[user] = sim_ui

			# n nearest users
			# n_users = sorted(user_similarity_index.items(), key=lambda x: x[1], reverse=True)[:N]
			n_users = review_users.items()[:N]

			sum_users = 0
			for user_i in n_users:
				user_id = user_i[0]
				rating_ir = review_users[user_id]
				baseline_ir = baseline_prediction[user_id][review_restaurant_id]
				sum_users += (rating_ir - baseline_ir) * temp_sim

				# user_id = user_i[0]
				# sim_ui = user_i[1]
				# rating_ir = review_users[user_id]
				# baseline_ir = baseline_prediction[user_id][review_restaurant_id]
				# sum_users += (rating_ir - baseline_ir) * sim_ui
	

			predicted_rating = baseline_ur + sum_users
			if review_user_id not in knn_prediction:
				knn_prediction[review_user_id] = {review_restaurant_id: predicted_rating}
			else:
				knn_prediction[review_user_id][review_restaurant_id] = predicted_rating

	print "Time after knn prediction: %d s" % (time() - start)
	# print knn_prediction['18kPq7GPye-YQ3LyKyAZPw']
	# Approach 2 -> topic modeling to cluster restaurants -> treat each cluster as individual restaurant

