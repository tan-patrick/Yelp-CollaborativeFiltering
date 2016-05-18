#!/usr/local/bin/python
# main restaurant recommendation program
import os
import sys
import json
from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.decomposition import LatentDirichletAllocation
import lda
from time import time

# path_to_repo = local path on your machine to project github repository
path_to_Dataset = os.path.dirname(os.path.abspath(__file__))
path_to_Dataset = path_to_Dataset.replace("TopicModeling", "Dataset")
# appends path_to_Dataset to search path for modules included below (i.e. users)
sys.path.append(path_to_Dataset)

import users
import restaurants
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

    # parameters for CountVectorizer
    # somewhat randomly chosen for now
    # for more explanation of the meaning of CountVectorizer()'s
    # arguments, see http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
    n_features = 10000

    # parameters for LDA
    # somewhat randomly chosen for now
    # for more explanation of the meaning of LatentDirichletAllocations()'s
    # arguments, see http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.LatentDirichletAllocation.html
    n_topics = 50
    maximum_iter = 50

    # load user data from appropriate file
    n_users = 10000
    user_data_path = "/users.json"
    stime = time()
    users = users.Users(path_to_Dataset + user_data_path, n_users=n_users)
    print ("Time to load all user data (except reviews): %d s" % (time() - stime))

    # build user_id => review dict for quick lookup
    reviews_data_path = "/reviews.json"
    stime = time()
    reviews = reviews.Reviews(path_to_Dataset + reviews_data_path)
    print ("Time to build fast look up user-reviews dict: %d s" % (time() - stime))

    #collected_reviews = dict()
    collected_reviews = list()
    restaurant_dict = dict()
    # for each user ...
    count = 0
    for user in users.list_users():
        # load all of user's restaurant reviews
        stime = time()
        uid = user.user_id()
        user_reviews = reviews.get_reviews_for_user(uid)
        if user_reviews == None:
            continue
        # key is now a (business_id, rating) tuple
        for key, value in user_reviews.items():
            business_id = key[0]
            rating = key[1]
            #collected_reviews[uid + ":" + business_id] = value
            #collected_reviews[count] = value
            collected_reviews.append(value)
            if business_id not in restaurant_dict:
                restaurant_dict[business_id] = list()
            restaurant_dict[business_id].append((count, rating))
            user.add_review(count, rating)
            count += 1
        
        # print ("Time to load reviews for user: %d s" % (time() - stime))
        # count = len(collected_reviews)
        # print ("Loading dictionary: %d of 1363242" % count)

    # build review-term matrix
    vocab_error = False
    stime = time()
    tf_vectorizer = CountVectorizer(stop_words='english', max_df=1.0, min_df=1, max_features=n_features)
    try:
        #tf = tf_vectorizer.fit_transform(collected_reviews.values())
        tf = tf_vectorizer.fit_transform(collected_reviews)
    except ValueError:
        # vocabulary, empty may only contain stop words
        vocab_error = True
        print ("No valid words")
    print ("Time to produce tf vector: %d s" % (time() - stime))
    if vocab_error:
        print ("No valid words")

    # run LDA on above matrix to generate ...
    stime = time()
    #model = LatentDirichletAllocation(n_topics=n_topics, learning_method='online', max_iter=maximum_iter, random_state=0)
    model = lda.LDA(n_topics=n_topics, n_iter=maximum_iter, random_state=0)
    model.fit(tf)
    #top_words = tf_vectorizer.get_feature_names()
    #print_top_words(model, top_words, 10)
    review_topic_matrix = model.transform(tf)
    print ("Time to apply LDA: %d s" % (time() - stime))

    # compute user-topic vectors
    # for each user U
        # initialize user-topic vector user_topic to 0s
        # for each review written by U
            # add corresponding review topic vector to user_topic,
            # scaled by rating/all of U's ratings
    stime = time()
    for user in users.list_users():
        user_topic = [0]*n_topics
        rating_sum = 0
        for review in user.reviews:
            idx = review[0]
            rating = review[1]
            rating_sum += rating
            user_topic = [sum(x) for x in zip(user_topic, [rating*y for y in review_topic_matrix[idx]])]
        #print ("rating sum = %d" % rating_sum)
        try:
            user_topic = [x/rating_sum for x in user_topic]
            #print user_topic
        except ZeroDivisionError:
            continue
        user.load_topic_vec(user_topic)
    print ("Time to compute user-topic vectors: %d s" % (time() - stime))

    # load all restaurant data 
    restaurant_data_path = "/restaurants.json"
    stime = time()
    restaurants = restaurants.Restaurants(path_to_Dataset + restaurant_data_path)
    print ("Time to load all restaurant data: %d s" % (time() - stime))

    # compute restaurant-topic vectors
    # for each restaurant R
        # initialize restaurant-topic vector restaurant_topic to 0s
        # for each review written about R
            # add corresponding review topic vector to restaurant_topic,
            # scaled by rating/all of R's ratings
    stime = time()
    #for restaurant_id, review_list in restaurant_dict.items():
    for restaurant in restaurants.list_restaurants():
        restaurant_topic = [0]*n_topics
        rating_sum = 0
        reviewed = True
        try:
            review_list = restaurant_dict[restaurant.business_id()]
        # if current restaurant has not been reviewed by at least one of n_users
        except KeyError:
            reviewed = False
            continue
        if reviewed == False:
            continue

        for review in review_list:
            idx = review[0]
            rating = review[1]
            rating_sum += rating
            restaurant_topic = [sum(x) for x in zip(restaurant_topic, [rating*y for y in review_topic_matrix[idx]])]
        try:
            restaurant_topic = [x/rating_sum for x in restaurant_topic]
            #print restaurant_topic
        except ZeroDivisionError:
            continue
        restaurant.load_topic_vec(restaurant_topic)
    print ("Time to compute restaurant-topic vectors: %d s" % (time() - stime))

