import numpy as np
import pandas as pd
from pymongo import MongoClient
import gridfs
import pickle

# Connect to your MongoDB instance
client = MongoClient("mongodb+srv://admin:ki6vpW0rEsx0HMt1@cluster0.e89k0jy.mongodb.net/?retryWrites=true&w=majority")
db = client["openit"]

my_collection_x_train = db["x_data"]
# Query the latest inserted document containing X_train data
X_train_document = my_collection_x_train.find_one({"X_train": {"$exists": True}}, sort=[("_id", -1)])

# Load X_train as a DataFrame
retrieved_X_train = pd.DataFrame(X_train_document["X_train"])

# Query the latest inserted document containing X_test data
X_test_document = my_collection_x_train.find_one({"X_test": {"$exists": True}}, sort=[("_id", -1)])

# Load X_test as a DataFrame
retrieved_X_test = pd.DataFrame(X_test_document["X_test"])

# Now you can use `retrieved_X_train` and `retrieved_X_test` for training, testing, or other purposes

# Get the collection
my_collection_y_data = db["y_data"]

# Query the latest inserted document containing y_train data
y_train_document = my_collection_y_data.find_one({"y_train": {"$exists": True}}, sort=[("_id", -1)])

# Load y_train as a NumPy array
retrieved_y_train = np.array(y_train_document["y_train"])

# Query the latest inserted document containing y_test data
y_test_document = my_collection_y_data.find_one({"y_test": {"$exists": True}}, sort=[("_id", -1)])

# Load y_test as a NumPy array
retrieved_y_test = np.array(y_test_document["y_test"])

# Now you can use `retrieved_y_train` and `retrieved_y_test` for training, testing, or other purposes

fs = gridfs.GridFS(db)
# Retrieve the model from MongoDB
model_file = fs.get_last_version(filename="random_forest_model")
model_binary = model_file.read()

# Load the model from the binary string
loaded_model = pickle.loads(model_binary)

# Now you can use `loaded_model` to make predictions, retrain, etc.

rf_model_preds = loaded_model.predict(retrieved_X_test)

from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.metrics import mean_squared_error

mse = mean_squared_error(retrieved_y_test, rf_model_preds)
# Calculate the mean absolute error of your Random Forest model on the validation data
print('Mean Absolute Error:', mean_absolute_error(retrieved_y_test, rf_model_preds))
print('Mean Squared Error:', mse)
print('Root Mean Squared Error:', np.sqrt(mean_squared_error(retrieved_y_test, rf_model_preds)))
score=r2_score(retrieved_y_test,rf_model_preds)
print(score)