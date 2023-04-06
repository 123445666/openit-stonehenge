import numpy as np
import pandas as pd
from pymongo import MongoClient
import gridfs
import pickle
import sys
from datetime import timedelta, date
from sklearn.ensemble import RandomForestRegressor

if __name__ == '__main__':  
    num = 0

    def auto_add_date(db, current_date):
        global num
        print(num)
        my_collection_consommation = db["consommations"]
        next_day = current_date + timedelta(days=num)
        num = num + 1
        print(next_day)
        print(next_day.strftime('%d-%m-%Y'))
        datacheck = my_collection_consommation.find_one({'data_date': next_day.strftime('%d-%m-%Y') })
        print(datacheck)
        if datacheck == None:
            predict_data(db, next_day)
        if(num < 15):
            auto_add_date(db, current_date)

    def predict_data(db, current_date): 
        Saison_Ete = False
        Saison_Hiver = False
        Saison_Printemps = False
        Normal_Day = False
        Weekend = False

        my_collection_consommation = db["consommations"]

        if month in [12, 1, 2]:
            Saison_Hiver = True
        elif month in [3, 4, 5]:
            Saison_Printemps = True
        elif month in [6, 7, 8]:
            Saison_Ete = True
        else:
            season = 'Automne'

        day_of_week = current_date.weekday()   
        
        if(day_of_week < 5):
            Normal_Day = True
        else:
            Weekend = True

        my_collection_daily = db["data_daily"]

        data_of_day = list(my_collection_daily.find({"Month": int(current_date.month)}))

        Pression = []
        Humidite = []
        Temperature = []

        # extract field values as a NumPy array
        Pression_values = np.array([d["Pression"] for d in data_of_day])

        # calculate the mean of the field
        Pression_mean = np.mean(Pression_values)

        # extract field values as a NumPy array
        Humidite_values = np.array([d["Humidite"] for d in data_of_day])

        # calculate the mean of the field
        Humidite_mean = np.mean(Humidite_values)

        # extract field values as a NumPy array
        Temperature_values = np.array([d["Temperature"] for d in data_of_day])

        # calculate the mean of the field
        Temperature_mean = np.mean(Temperature_values)

        #https://www.meteosource.com/api/v1/free/point?place_id=Montpellier&sections=current%2Chourly&language=en&units=auto&key=89ivg44q9w8rsv6zyqype3pd1rqztvstsmrwzlac
        #Using API to get the data pressure, humidity, temperature (units: metric) (Next Step)

        data_of_day = my_collection_daily.find_one({"Day": int(day), "Month": int(month)})
        if data_of_day != None:
            Pression.append(data_of_day["Pression"])
            Humidite.append(data_of_day["Humidite"])
            Temperature.append(data_of_day["Temperature"])
        else:
            Pression.append(Pression_mean)
            Humidite.append(Humidite_mean)
            Temperature.append(Temperature_mean)

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

        #fs = gridfs.GridFS(db)
        # Retrieve the model from MongoDB
        #model_file = fs.get_last_version(filename="random_forest_model")
        #model_binary = model_file.read()

        print('loading pickle')
        # Load the model from the binary string
        #loaded_model = pickle.loads(model_binary)

        # Now you can use `loaded_model` to make predictions, retrain, etc.

        #rf_model_preds = loaded_model.predict(retrieved_X_test)

        # Define the model. Set random_state to 1
        rf_model = RandomForestRegressor(n_estimators=100)

        # fit your model
        rf_model.fit(retrieved_X_train, retrieved_y_train)

        #model_binary = pickle.dumps(rf_model)

        #model_id = fs.put(model_binary, filename="random_forest_model")
        #print(f"Model saved with ID: {model_id}")

        # Example weather data for a future day
        # Replace these values with the actual weather data
        future_consommation_data = {
            'Pression au niveau mer': Pression,
            'Humidité': Humidite,
            'Température (°C)': Temperature,
            'Saison_Ete': [Saison_Ete],
            'Saison_Hiver': [Saison_Hiver],
            'Saison_Printemps': [Saison_Printemps],
            'Normal_Day': [Normal_Day],
            'Weekend': [Weekend],
            'Day': [day],
            'Month': [month]
        }

        # Convert the dictionary to a DataFrame
        future_consommation_df = pd.DataFrame.from_dict(future_consommation_data)
        # Make predictions using the trained model
        future_consommation_preds = rf_model.predict(future_consommation_df)
        print(future_consommation_preds)
        # Print the predictions
        for sum_consommation_by_date in future_consommation_preds:
                my_collection_consommation.insert_one({'data_date': current_date.strftime('%d-%m-%Y'), 'consommation': sum_consommation_by_date})

        return
     
    data_date = sys.argv[1]

    # Connect to your MongoDB instance
    client = MongoClient("mongodb+srv://admin:ki6vpW0rEsx0HMt1@cluster0.e89k0jy.mongodb.net/?retryWrites=true&w=majority")
    db = client["openit"]

    array_date = data_date.split('-')

    day = array_date[0]
    month = array_date[1]
    year = array_date[2]

    predire_date = date(int(year), int(month), int(day))

    auto_add_date(db, predire_date)