#!/usr/local/bin/python
# extract all restaurant reviews from all business reviews and write to reviews.json file
# done for preprocessing
import json
import restaurants
import random

# get list of restaurants, build restaurant_id-->name dict
# iterate through list of reviews, checking if corresponding
# business_id is a restaurant
# if so, write json back to reviews.json file

if __name__ == '__main__':
	# get all restaurants from restaurants.json file
	restaurants = restaurants.Restaurants("restaurants.json")
	
	restaurant_dict = dict()
	
	# build business_id-->restaurant_name dictionary for quick lookup
	for r in restaurants.list_restaurants():
		restaurant_dict[r.business_id()] = r.name()
	
	training_reviews_fp = open("reviews.json", 'w')
	test_reviews_fp = open("test_reviews.json", 'w')

	# iterate through all reviews and only write restaurant reviews to "reviews.json"	
	reviews_data_file = "./yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json"
	with open(reviews_data_file, 'r') as rf:
		for entry in rf:
			review = json.loads(entry)
			if restaurant_dict.get(review['business_id']):
				validation = random.random()
				if validation <= .9:
					training_reviews_fp.write(entry)
				else:
					test_reviews_fp.write(entry)
	
	training_reviews_fp.close()
	test_reviews_fp.close()
