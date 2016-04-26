#!/usr/bin/python
# python script to extract restaurants from yelp business data and write to new json file
import json

if __name__ == "__main__":

	# open yelp business data file and restaurant data file
	restaurants_file = "restaurants.json"
	biz_data_fp = open("yelp_academic_dataset_business.json", 'r')
	restaurant_data_fp = open(restaurants_file, 'w')

	# write all restaurants in business data file to restaurant file
	for line in biz_data_fp:
		business = json.loads(line)
		for category in business["categories"]:
			if category == "Restaurants":
				restaurant_data_fp.write(line)
	
	restaurant_data_fp.close()
	biz_data_fp.close()
