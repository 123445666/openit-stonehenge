# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import pymongo
import gridfs
import pickle

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/mnt/f/Data/TiengPhap/Keyce/KitGame2/Code/openit-stonehenge/python/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import seaborn as sns
import matplotlib.pyplot as plt

# Mongo init
client = pymongo.MongoClient("mongodb+srv://admin:ki6vpW0rEsx0HMt1@cluster0.e89k0jy.mongodb.net/?retryWrites=true&w=majority")
db = client["openit"]
fs = gridfs.GridFS(db)

my_collection = db["data"]

df = pd.read_csv("/mnt/f/Data/TiengPhap/Keyce/KitGame2/Code/openit-stonehenge/python/input/donnees.csv")
print("Number of rows: " + str(df.shape[0]))
print("Number of columns: " + str(df.shape[1]))
df.columns

df.fillna(df.mean(numeric_only=True), inplace=True)

# Assurez-vous que la colonne "Date_Heure" est au format datetime
df['Date_Heure'] = pd.to_datetime(df['Date_Heure'])

# Créez des colonnes pour l'heure de la journée, le jour, le mois et l'année
df['Hour'] = df['Date_Heure'].dt.hour
df['Day'] = df['Date_Heure'].dt.day
df['Month'] = df['Date_Heure'].dt.month
df['Year'] = df['Date_Heure'].dt.year
df['DayOfWeek'] = df['Date_Heure'].dt.dayofweek

df = df.drop(['index','Periode de mesure de la rafale'], axis=1)

# Define a function to map the month to a season
def get_season(month):
    if month in [12, 1, 2]:
        return 'Hiver'
    elif month in [3, 4, 5]:
        return 'Printemps'
    elif month in [6, 7, 8]:
        return 'Ete'
    else:
        return 'Automne'

# Add a season column to the dataframe
df['Saison'] = df['Month'].map(get_season)

# Perform one-hot encoding on the Season column
season_dummies = pd.get_dummies(df['Saison'], prefix='Saison')

# Add the one-hot encoded columns to the original dataframe
df = pd.concat([df, season_dummies], axis=1)

condition = lambda row: 1 if (row['DayOfWeek'] >= 0) and (row['DayOfWeek'] <= 4) else 0
df['Normal_Day'] = df.apply(condition, axis=1)

condition = lambda row: 1 if (row['DayOfWeek'] == 5) or (row['DayOfWeek'] == 6) else 0
df['Weekend'] = df.apply(condition, axis=1)

condition = lambda row: 1 if (row['Hour'] >= 5) and (row['Hour'] <= 12) else 0
df['Matin'] = df.apply(condition, axis=1)

condition = lambda row: 1 if (row['Hour'] >= 13) and (row['Hour'] <= 19) else 0
df['Apresmidi'] = df.apply(condition, axis=1)

condition = lambda row: 1 if (row['Hour'] >= 20) or (row['Hour'] <= 4) else 0
df['Nuit'] = df.apply(condition, axis=1)

hourly_data= df.groupby(['Hour', 'Day', 'Month']).agg({'consommation': 'mean', 'Température (°C)': 'mean',
     'Pression au niveau mer' : 'mean', 'Humidité' : 'mean'}).reset_index()

# Insert data into the MongoDB collection
my_collection_hour = db["data_hour"]
my_collection_hour.delete_many({})
my_collection_hour.insert_many(hourly_data.to_dict('records'))

month_data= df.groupby(['Month']).agg({'consommation': 'mean', 'Température (°C)': 'mean',
     'Pression au niveau mer' : 'mean', 'Humidité' : 'mean'}).reset_index()
# Insert data into the MongoDB collection
my_collection_month = db["data_month"]
my_collection_month.delete_many({})
my_collection_month.insert_many(month_data.to_dict('records'))

day_data= df.groupby(['Day', 'Month']).agg({'consommation': 'mean', 'Température (°C)': 'mean',
     'Pression au niveau mer' : 'mean', 'Humidité' : 'mean'}).reset_index()
# Insert data into the MongoDB collection
my_collection_day = db["data_day"]
my_collection_day.delete_many({})
my_collection_day.insert_many(day_data.to_dict('records'))

feature_columns = ['Pression au niveau mer', 'Humidité', 'Température (°C)', 
                   'Saison_Ete', 'Saison_Hiver', 'Saison_Printemps', 'Normal_Day', 
                   'Weekend', 'Hour', 'Day', 'Month', 'Year', 'consommation']

df = df[feature_columns]

# Split the data
X = df.drop("consommation", axis=1)
y = df["consommation"]

X_train, X_test,y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=0)

my_collection_x_train = db["x_data"]
my_collection_x_train.delete_many({})
# Convert X_train and X_test to lists of dictionaries
X_train_list = X_train.to_dict(orient="records")
X_test_list = X_test.to_dict(orient="records")

# Insert X_train and X_test into MongoDB as documents
X_train_data_document = {"X_train": X_train_list}
X_test_data_document = {"X_test": X_test_list}

result = my_collection_x_train.insert_one(X_train_data_document)
result = my_collection_x_train.insert_one(X_test_data_document)

my_collection_y_data = db["y_data"]
my_collection_y_data.delete_many({})
# Convert y_train to a list and insert it into MongoDB as a document
y_train_list = y_train.tolist()
y_training_data_document = {"y_train": y_train_list}
result = my_collection_y_data.insert_one(y_training_data_document)

# Convert y_test to a list and insert it into MongoDB as a document
y_test_list = y_test.tolist()
y_test_data_document = {"y_test": y_test_list}
result = my_collection_y_data.insert_one(y_test_data_document)

print(f"Inserted y_test data with ID: {result.inserted_id}")

# Define the model. Set random_state to 1
rf_model = RandomForestRegressor(n_estimators=100)

# fit your model
rf_model.fit(X_train, y_train.values.ravel())
rf_model_preds = rf_model.predict(X_test)

model_binary = pickle.dumps(rf_model)

model_id = fs.put(model_binary, filename="random_forest_model")
print(f"Model saved with ID: {model_id}")

from sklearn.metrics import mean_absolute_error, r2_score
mse = mean_squared_error(y_test, rf_model_preds)
# Calculate the mean absolute error of your Random Forest model on the validation data
print('Mean Absolute Error:', mean_absolute_error(y_test, rf_model_preds))
print('Mean Squared Error:', mse)
print('Root Mean Squared Error:', np.sqrt(mean_squared_error(y_test, rf_model_preds)))
score=r2_score(y_test,rf_model_preds)
print(score)

