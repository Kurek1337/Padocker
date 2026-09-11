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

    results_url = f"https://api.openf1.org/v1/session_result?session_key={session_key}"
    results_response = requests.get(results_url, timeout=30)
    results_data = results_response.json()


    print("Grid status code:", grid_response.status_code)

    if isinstance(grid_data, list):
        grid_df = pd.DataFrame(grid_data)

        print(grid_df.head())
        print(grid_df.columns)

    else:
        print("No starting grid data available:")
        print(grid_data)

    if isinstance(drivers_data, list):
        drivers_df = pd.DataFrame(drivers_data)
    else:
        print("No drivers avaible")

    if isinstance(results_data, list):
        results_df = pd.DataFrame(results_data)
        results_df = results_df.rename(columns={"position": "finish_position"})
        print("working")
    else:
        print("No results available")

    #results_df = results_df.rename(columns={"position": "finish_position"})
    print("Results here")
    print(results_df.head())
    print(results_df.columns)

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


race_df = pd.merge(
    drivers_df,
    results_df,
    on=["driver_number", "session_key", "meeting_key"]
)

race_df = race_df[
    [
        "meeting_key",
        "session_key",
        "driver_number",
        "full_name",
        "team_name",
        "finish_position",
        "number_of_laps",
        "points",
        "dnf",
        "dns",
        "dsq"
    ]
]

race_df["finished_in_points"] = (race_df["points"] > 0).astype(int)
print("merged here -----")
print(race_df.head())
print(race_df.columns)

selected_session = sessions_df[
    sessions_df["session_key"] == session_key
].iloc[0]

race_df["year"] = selected_session["year"]
race_df["circuit_name"] = selected_session["circuit_short_name"]
race_df["race_date"] = selected_session["date_start"]



print("FINAL RACE DATA:")
print(race_df.head())
print(race_df.columns)

race_df.to_csv("Bahrain-2023.csv", index=False)
# PredictedPosition = 10 # Initial hard-coded value for tests 
# After qualifying, predict whether a driver will finish in points (TOP 10)
# driverFinishInPoints = 1 if PredictedPosition <= 10 else 0 # Binary Classification 

