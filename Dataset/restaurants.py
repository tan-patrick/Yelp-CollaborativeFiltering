# Restaurant and Restaurants classes for restaurant data
import json

class Restaurant(object):

    # json_obj = restaurant's json object from data file
    def __init__(self, json_obj):
        self.restaurant = json.loads(json_obj)
        self.topic_vec = list()

    def business_id(self):
        return self.restaurant['business_id']

    def name(self):
        return self.restaurant['name']

    def address(self):
        return self.restaurant['full_address']

    def city(self):
        return self.restaurant['city']

    def state(self):
        return self.restaurant['state']

    def stars(self):
        return self.restaurant['stars']

    def review_count(self):
        return self.restaurant['review_count']

    def categories(self):
        return self.restaurant['categories']

    def open(self):
        return self.restaurant['open']

    def hours(self):
        return self.restaurant['hours']

    def attributes(self):
        return self.restaurant['attributes']

    # load restaurant-topic vector
    def load_topic_vec(self, topic_vec):
        self.topic_vec = topic_vec

class Restaurants(object):

    def __init__(self, restaurants_file):
        self.restaurants = list()
        self.load_restaurants(restaurants_file)

    # add a restaurant to the list of restaurants
    def add(self, restaurant):
        self.restaurants.append(restaurant)

    # load all restaurants into Restaurants class from restaurants_file
    def load_restaurants(self, restaurants_file):
        with open(restaurants_file, 'r') as rf:
            for entry in rf:
                restaurant = Restaurant(entry)
                self.add(restaurant)

    # return the list of restaurants
    def list_restaurants(self):
        return self.restaurants

