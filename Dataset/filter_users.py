#!/usr/local/bin/python
# python script to extract only users who have written reviews from all users in dataset and write to new json file
# done for preprocessing of data
import json
import reviews
from time import time

if __name__ == "__main__":

    # open yelp business data file and users data file
    filtered_users_file = "users.json"
    user_data_file = "./yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_user.json"
    user_data_fp = open(user_data_file, 'r')
    filtered_users_fp = open(filtered_users_file, 'w')

    # be sure to have run filter_reviews.py before running this script
    stime = time()
    restaurant_reviews = reviews.Reviews("reviews.json") 
    print ("time to build restaurant reviews: %d s" % (time() - stime))

    # write all restaurants in business data file to restaurant file
    count = 0
    for line in user_data_fp:
        print ("user %d" % count)
        user = json.loads(line)
        if restaurant_reviews.user_has_written_review(user['user_id']):
            filtered_users_fp.write(line)
        count += 1
    
    filtered_users_fp.close()
    user_data_fp.close()
