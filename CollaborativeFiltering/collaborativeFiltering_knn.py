import os
import sys
import json
import math
import csv
from time import time
from sklearn.metrics.pairwise import cosine_similarity

path_to_Dir= os.path.dirname(os.path.abspath(__file__))
path_to_Dataset = path_to_Dir.replace("CollaborativeFiltering", "Dataset")
path_to_TopicModeling = path_to_Dir.replace("CollaborativeFiltering", "TopicModeling")
sys.path.append(path_to_Dataset)
sys.path.append(path_to_TopicModeling)

import restaurants
from evaluation import compute_rmse

if __name__ == '__main__':
	start = time()
	restaurant_rating = {} #{restaurantid1:4.0,restaurantid2:3.5}
	user_average_rating = {} #{userid1:4.0,userid2:3.5...}
	baseline_prediction = {} #{userid1:{restaurant1:1.1, restaurant2:3.0,...}...}
	knn_prediction = {} #{userid1:{restaurant1:1.1, restaurant2:3.0,...}...}
	restaurant_index = {} #{restaurant1: {user1: 4.0,..}} -> {restaurant1: [user1,user2...]}
	user_index = {} #{userid1:{restaurant1:1.1, restaurant2:3.0,...}...}

	restaurant_data_path = "/restaurants.json"
	user_data_path = "/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_user.json"
	# user_data_path = "../../spark-1.6.0-bin-hadoop2.6/249_CloudComputing/data/yelp_academic_dataset_user.json"
	review_data_path = "/test_reviews.json"
	user_topic_matrix_data_path = '/user_topic_matrix_all_users.csv'

	# compute the average rating of all restaurants by all users -> average_restaurants_rating
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
	with open(user_data_path, 'r') as uf:
		for entry in uf:
			user = json.loads(entry)
			user_id = user['user_id']
			average_rating = user['average_stars']
			user_average_rating[user_id] = average_rating
	print "Time after constructing user rating index: %d s" % (time() - start)

	# compute baseline prediction rating as predicted_rating = average_restaurants_rating + bias_user + bias_restaurant
	with open(path_to_Dataset + review_data_path, 'r') as rf:
		for entry in rf:
			review = json.loads(entry)
			actual_rating = review['stars']
			review_user_id = review['user_id']
			review_restaurant_id = review['business_id']
			review_user_average_rating = user_average_rating[review_user_id]
			review_restaurant_rating = restaurant_rating[review_restaurant_id]	
			predicted_rating = average_restaurants_rating + (review_user_average_rating-average_restaurants_rating) + (review_restaurant_rating-average_restaurants_rating)
			if review_user_id not in baseline_prediction:
				baseline_prediction[review_user_id] = {review_restaurant_id: (actual_rating, predicted_rating)}
			else:
				baseline_prediction[review_user_id][review_restaurant_id] = (actual_rating, predicted_rating)

			# construct restaurant index for later use
			review_rating = review['stars']
			if review_restaurant_id not in restaurant_index:
				# restaurant_index[review_restaurant_id] = {review_user_id: review_rating}
				restaurant_index[review_restaurant_id] = [review_user_id]
			else:
				# restaurant_index[review_restaurant_id][review_user_id] = review_rating
				restaurant_index[review_restaurant_id].append(review_user_id)

			# construct user index for later use
			if review_user_id not in user_index:
				user_index[review_user_id] = {review_restaurant_id: review_rating}
			else:
				user_index[review_user_id][review_restaurant_id] = review_rating

	print baseline_prediction['tC62PSePYtPwSKc6Asf7rQ']
	print baseline_prediction['rkmM0Ku4NmG6gE5DaaEntA']
	print "Time after baseline prediction: %d s" % (time() - start)

	rmse_baseline = compute_rmse(baseline_prediction)
	print rmse_baseline #1.10317
	print "Time after evaluation: %d s" % (time() - start)

	# construct user_topic_matrix
	user_topic_matrix = {} # {user1: [matrix],user2: [matrix]}
	with open(path_to_TopicModeling + user_topic_matrix_data_path, 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			user_topic_matrix[row[0]] = row[1:]
	print "Time after constructing user_topic_matrix: %d s" % (time() - start)

	# predict how user u would rate on restaurant r by knn
	# find N nearest users who has rated r
	# r_predict = baseline_ur + all N users as user i sum(r_ir - baseline_ir ) * similarity(ui)
	N = 2
	count = 0
	with open(path_to_Dataset + review_data_path, 'r') as rf:
		for entry in rf:
			count += 1
			if count % 10000 == 0:
				print "Process number " + str(count)
				print "Process time: %d s" % (time() - start)

			review = json.loads(entry)
			actual_rating = review['stars']
			review_user_id = review['user_id']
			review_restaurant_id = review['business_id']
			baseline_ur = baseline_prediction[review_user_id][review_restaurant_id][1]

			# users that rated this restaurant
			review_users = restaurant_index[review_restaurant_id]

			# compute similarity 
			user_topic_i_list = []
			user_similarity_index = {}
			user_topic_u = [user_topic_matrix[review_user_id]]
			for user in review_users:
				user_topic_i_list.append(user_topic_matrix[user])
			similarity_vector = cosine_similarity(user_topic_u, user_topic_i_list)[0]
			similarity_vector_index = zip(review_users, similarity_vector) # [(u1,0.5),(u2,0.3)...]

			# n nearest users
			n_users = sorted(similarity_vector_index, key=lambda x: x[1], reverse=True)[:N]

			sum_users = 0
			for user_i in n_users:
				user_id = user_i[0]
				sim_ui = user_i[1]
				rating_ir = user_index[user_id][review_restaurant_id]
				baseline_ir = baseline_prediction[user_id][review_restaurant_id][1]
				sum_users += (rating_ir - baseline_ir) * sim_ui
	
			predicted_rating = baseline_ur + sum_users
			if review_user_id not in knn_prediction:
				knn_prediction[review_user_id] = {review_restaurant_id: (actual_rating, predicted_rating)}
			else:
				knn_prediction[review_user_id][review_restaurant_id] = (actual_rating, predicted_rating)

	print "Time after knn prediction: %d s" % (time() - start)

	rmse_knn = compute_rmse(knn_prediction)
	print rmse_knn # 0.799371312757
	print "RMSE Knn: " + str(rmse_knn)
	print "RMSE Baseline: " + str(rmse_baseline)
	print "Time after evaluation: %d s" % (time() - start)
	# Approach 2 -> topic modeling to cluster restaurants -> treat each cluster as individual restaurant

