import pymongo
import random

"""
Prototype distance calculator and sorter that could be used to return nearby posts within a max distance if we have the 
coordinates of the pickup locations and the user location.
"""


# Connect to MongoDB
myclient = pymongo.MongoClient("mongodb+srv://charley:8nCc9Wq4FUDBkgyx@hackku24.eum715g.mongodb.net/?retryWrites=true&w=majority&appName=HackKU24")

# Access the database
mydb = myclient["mydatabase"]
mycol = mydb["foods"]

# Create a 2dsphere index on the location field so the location sort works
mycol.create_index([("post.location", "2dsphere")])

# For now, this is just populating the database with random locations around the query location
for n in range(10):
    restaurant_document = {
        "name": f"Test{n}",
        "post": {
            "food_description": "Delicious food",
            "servings": 10,
            "location": {
                "type": "Point",
                "coordinates": [-94.138251 + random.randint(-100, 100)/100, 38.983148 + random.randint(-100, 100)/100]
            }
        }
    }

    # Insert the restaurant document into the collection
    mycol.insert_one(restaurant_document)

# Define a (current) location (longitude and latitude) for the query
query_location = {
    "coordinates": [float(-96.25), float(38.97)]
}

# Find restaurants near the query location within a specified radius (in meters)
near_query = {
    "$nearSphere": {
        "$geometry": {
            "type": "Point",
            "coordinates": [-96, 39]  # [longitude, latitude]
        },
        "$maxDistance": 20000  # Specify the maximum distance in meters
    }
}

nearby_restaurants = mycol.find({"post.location": near_query })

print(nearby_restaurants)

# This prints the restaurants, but it could easily return them if given a GET request with the query location
for restaurant in nearby_restaurants:
    print(restaurant)