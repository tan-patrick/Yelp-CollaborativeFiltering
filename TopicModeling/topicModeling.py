#!/usr/bin/python
# main restaurant recommendation program

import os
import sys

# path_to_repo = local path on your machine to project github repository
path_to_Dataset = os.path.dirname(os.path.abspath(__file__))
path_to_Dataset = path_to_Dataset.replace("TopicModeling", "Dataset")
# appends path_to_Dataset to search path for modules included below (i.e. users)
sys.path.append(path_to_Dataset)

import users

if __name__ == '__main__':

	# load users and restaurants from appropriate files
	users = users.Users(path_to_Dataset + "/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_user.json")
	# for each user ...
	for user in users.list_users():
		# load all of user's restaurant reviews
		user.load_reviews(path_to_Dataset + "/reviews.json")
		sys.exit()
		# build review term matrix
		# run LDA on above matrix to generate ...
		# ... topic-term matrix
		# topic-term matrix represents usres's topics ...
		# ... of interest

	# compute users similarities

	# use similarity above w/ CF to generate recommendations
