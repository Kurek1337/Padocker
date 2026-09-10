import requests
import pandas as pd 
from pprint import pprint 


url = "https://api.openf1.org/v1/sessions?year=2023&session_name=Race"

response = requests.get(url, timeout = 30)

print("Status code", response.status_code)

data = response.json()

if isinstance(data, list):
    sessions_df = pd.DataFrame(data)

    session_key = sessions_df.iloc[0]["session_key"]
    print("Selected session:", session_key)

    drivers_url = f"https://api.openf1.org/v1/drivers?session_key={session_key}"
    drivers_response = requests.get(drivers_url, timeout=30)
    drivers_data = drivers_response.json()

    grid_url = f"https://api.openf1.org/v1/starting_grid?session_key={session_key}"
    grid_response = requests.get(grid_url, timeout=30)
    grid_data = grid_response.json()


    print("Grid status code:", grid_response.status_code)

    if isinstance(grid_data, list):
        grid_df = pd.DataFrame(grid_data)

        print(grid_df.head())
        print(grid_df.columns)

    else:
        print("No starting grid data available:")
        print(grid_data)


    drivers_df = pd.DataFrame(drivers_data)

    print(sessions_df[["circuit_short_name", "date_start", "session_key"]])

    print(sessions_df.head())
    print(sessions_df.columns)

    print (drivers_df.head())
    print (drivers_df.columns)

   
    #df.to_csv("Sessions-2023.csv", index = False)
    #print("CSV created successfully.")
else:
    print("The API returned an error:")
    print(data)






# PredictedPosition = 10 # Initial hard-coded value for tests 
# After qualifying, predict whether a driver will finish in points (TOP 10)
# driverFinishInPoints = 1 if PredictedPosition <= 10 else 0 # Binary Classification 

