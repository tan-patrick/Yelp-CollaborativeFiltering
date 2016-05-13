#!/usr/local/bin/python
# main restaurant recommendation program
import os
import sys
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from time import time

# path_to_repo = local path on your machine to project github repository
path_to_Dataset = os.path.dirname(os.path.abspath(__file__))
path_to_Dataset = path_to_Dataset.replace("TopicModeling", "Dataset")
# appends path_to_Dataset to search path for modules included below (i.e. users)
sys.path.append(path_to_Dataset)

import users
import reviews

def print_top_words(model, feature_names, n_top_words):
	for topic_idx, topic in enumerate(model.components_):
		test = topic.argsort()[:-n_top_words - 1:-1]
		print("Topic #%d:" % topic_idx)
		print(" ".join([feature_names[i]
						for i in topic.argsort()[:-n_top_words - 1:-1]]))
		print(" ".join(str([topic[i]
						for i in topic.argsort()[:-n_top_words - 1:-1]])))
	print()

if __name__ == '__main__':

	# load users and restaurants from appropriate files
	n_users = 10000
	user_data_path = "/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_user.json"
	stime = time()
	users = users.Users(path_to_Dataset + user_data_path, n_users=n_users)
	print ("Time to load all user data (except reviews): %d s" % (time() - stime))

	# build user_id => review dict for quick lookup
	reviews_data_path = "/reviews.json"
	stime = time()
	reviews = reviews.Reviews(path_to_Dataset + reviews_data_path)
	print ("Time to build fast look up user-reviews dict: %d s" % (time() - stime))

	# parameters for CountVectorizer
	# somewhat randomly chosen for now
	# for more explanation of the meaning of CountVectorizer()'s
	# arguments, see http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
	n_features = 2000

	# parameters for LDA
	# somewhat randomly chosen for now
	# for more explanation of the meaning of LatentDirichletAllocations()'s
	# arguments, see http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.LatentDirichletAllocation.html
	n_topics = 100
	maximum_iter = 5

	collected_reviews = dict()
	# for each user ...
	count = 0;
	for user in users.list_users():
		# load all of user's restaurant reviews
		stime = time()
		uid = user.user_id()
		user_reviews = reviews.get_reviews_for_user(uid)
		if user_reviews == None:
			continue
		for key, value in user_reviews.items():
			collected_reviews[uid + ":" + key] = value
		# print ("Time to load reviews for user: %d s" % (time() - stime))
		count = len(collected_reviews)
		print ("Loading dictionary: %d of 1363242" % count)

	# build review-term matrix
	vocab_error = False
	stime = time()
	tf_vectorizer = CountVectorizer(stop_words='english', max_df=1.0, min_df=1, max_features=n_features)
	try:
		tf = tf_vectorizer.fit_transform(collected_reviews.values())
	except ValueError:
		# vocabulary, empty may only contain stop words
		vocab_error = True
		print ("No valid words")
	print ("Time to produce tf vector: %d s" % (time() - stime))
	if vocab_error:
		print ("No valid words")

	# run LDA on above matrix to generate ...
	stime = time()
	lda = LatentDirichletAllocation(n_topics=n_topics, learning_method='online', max_iter=maximum_iter, random_state=0)
	# topic_term_matrix = lda.fit_transform(tf)
	lda.fit(tf)
	top_words = tf_vectorizer.get_feature_names()
	print_top_words(lda, top_words, 10)
	print ("Time to apply LDA: %d s" % (time() - stime))
	#print

	# user.load_topics(topic_term_matrix)
	# ... topic-term matrix
	# topic-term matrix represents users's topics ...
	# ... of interest


	# compute users similarities

	# use similarity above w/ CF to generate recommendations

