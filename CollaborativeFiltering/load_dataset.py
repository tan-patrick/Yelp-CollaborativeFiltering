import random
from sets import Set
from classes import Rating, RatingSet

def split_ratings(ratings, target_percentage=0.10):
    seen_users = Set()
    seen_items = Set()
    training_set = []
    test_set = []
    random.shuffle(ratings)
    for rating in ratings:
        if rating.user in seen_users and rating.item in seen_items and len(test_set) < target_percentage * len(ratings):
            test_set.append(rating)
        else:
            training_set.append(rating)
        seen_users.add(rating.user)
        seen_items.add(rating.item)
    return training_set, test_set

def load_dataset(split_ratio=0.10):
    print("Using movie data in ml-1m folder...")
    movie_file_name = "./ml-1m/movies.dat"
    ratings_file_name = "./ml-1m/ratings.dat"
    original_id_to_movie = {}
    movie_count = sum(1 for line in open(movie_file_name))
    # print movie_count
    for line in open(movie_file_name):
        split_line = line.split("::")
        original_id_to_movie[split_line[0]] = split_line[1]
    # print original_id_to_movie

    ratings = []
    item_to_index = {}
    user_to_index = {}
    ratings_count = sum(1 for line in open(ratings_file_name))

    for line in open(ratings_file_name):
        user, movie, rating, timestamp = line.split("::")
        item = original_id_to_movie[movie]
        #planning to remove _to_index lists
        if user not in user_to_index:
            user_index = user_to_index[user] = len(user_to_index)
        if item not in item_to_index:
            item_index = item_to_index[item] = len(item_to_index)
        ratings.append(Rating(user_index,item_index, float(rating)))
    training_set, test_set = split_ratings(ratings, split_ratio)
    return RatingSet(training_set, test_set, user_to_index, item_to_index)

if __name__ == "__main__":
    rating_set = load_dataset()

