# User and Users classes for user data
import json

class User(object):

    # json_obj = user's json object from user data file
    def __init__(self, json_obj):
        self.user = json.loads(json_obj)
        self.reviews = list()
        self.topic_vec = list()
        self.review_count = 0

    def user_id(self):
        return self.user['user_id']
        
    def name(self):
        return self.user['name']

    def review_count(self):
        #return self.user['review_count']
        return self.review_count

    def average_stars(self):
        return self.user['average_stars']

    def votes(self):
        return self.user['votes']

    def friends(self):
        return self.user['friends']

    def elite(self):
        return self.user['elite']

    def compliments(self):
        return self.user['compliments']

    def fans(self):
        return self.user['fans']

    def topic_vec(self):
        return self.topic_vec
    
    def add_review(self, idx, stars):
        self.reviews.append((idx, stars))
        self.review_count += 1

    # topic-term matrix from LDA
    def load_topic_vec(self, topic_vec):
        self.topic_vec = topic_vec
            

class Users(object):

    # n_users = number of users loaded from user data file
    def __init__(self, user_data_file, n_users=1000):
        self.users = list()
        self.load_users(user_data_file, n_users)

    # add user to list of users
    def add(self, user):
        self.users.append(user)

    # return the list of users
    def list_users(self):
        return self.users

    # load all users into Users class from user_data_file    
    def load_users(self, user_data_file, n_users=1000):
        with open(user_data_file, 'r') as uf:
            i = 0
            for entry in uf:
                if i == n_users:
                    break
                user = User(entry)
                self.add(user)
                i = i + 1
