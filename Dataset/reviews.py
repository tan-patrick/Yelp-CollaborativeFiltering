# Reviews class for reviews data
import json

class Reviews(object):
    
    def __init__(self, reviews_file):
        # maps user_id's to their reviews
        self.reviews = dict() # { user_id => { (business_id, rating) => review_text } }
        self.load_reviews(reviews_file)

    # load reviews from reviews.json file
    def load_reviews(self, reviews_file):
        count = 1;
        with open(reviews_file, 'r') as rf:
            for entry in rf:
                #print("Loading from file: %d of 1363242" % count)
                count = count + 1
                review = json.loads(entry)
                user_id = review['user_id']
                restaurant_review = (review['business_id'], review['stars'])
                if user_id not in self.reviews:
                    self.reviews[user_id] = dict()
                self.reviews[user_id][restaurant_review] = review['text']

    # return dictionary of business_id => review_text for each of
    # the restaurants reviewed by uid
    def get_reviews_for_user(self, uid):
        try:
            return self.reviews[uid]
        except KeyError:
            return None

    # returns True if user has written a restaurant review, False otherwise
    def user_has_written_review(self, uid):
        return (uid in self.reviews)
            
