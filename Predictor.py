import requests
import pandas as pd 
from pprint import pprint 

url = "https://api.openf1.org/v1/sessions?year=2023&session_name=Race"

response = requests.get(url, timeout = 30)

print("Status code", response.status_code)

data = response.json()

if isinstance(data, list):
    df = pd.DataFrame(data)

    print(df.head())
    print(df.columns)

    df.to_csv("Sessions-2023.csv", index = False)
    print("CSV created successfully.")
else:
    print("The API returned an error:")
    print(data)






PredictedPosition = 10 # Initial hard-coded value for tests 
# After qualifying, predict whether a driver will finish in points (TOP 10)
driverFinishInPoints = 1 if PredictedPosition >= 10 else 0 # Binary Classification 

