import requests
import pandas as pd 
from pprint import pprint 
import time


url = "https://api.openf1.org/v1/sessions?year=2023&session_name=Race"

response = requests.get(url, timeout = 30)

print("Status code", response.status_code)

data = response.json()

if isinstance(data, list):
    sessions_df = pd.DataFrame(data)

    all_races = []
    for _, session in sessions_df.iterrows():

        session_key = session["session_key"]

        print(
        "Processing:",
        session["circuit_short_name"],
        session_key
        )

        if session["is_cancelled"]:
            print("Skipping cancelled race")
            continue
        

        
        

        
        print("Selected session:", session_key)

        ####################
        #Drivers
        ####################

        drivers_url = f"https://api.openf1.org/v1/drivers?session_key={session_key}"
        drivers_response = requests.get(drivers_url, timeout=30)
        drivers_data = drivers_response.json()
        time.sleep(2.1)
        ####################
        #Grid
        ####################

        grid_url = f"https://api.openf1.org/v1/starting_grid?session_key={session_key}"
        grid_response = requests.get(grid_url, timeout=30)
        grid_data = grid_response.json()
        time.sleep(2.1)
        ####################
        #Results
        ####################

        results_url = f"https://api.openf1.org/v1/session_result?session_key={session_key}"
        results_response = requests.get(results_url, timeout=30)
        results_data = results_response.json()
        time.sleep(2.1)
        ####################
        #Data Checks
        ####################
        print("Grid status code:", grid_response.status_code)

        if isinstance(grid_data, list):
            grid_df = pd.DataFrame(grid_data)

            print(grid_df.head())
            print(grid_df.columns)
        else:
            print("No starting grid data available:")
            print(grid_data)


        if not isinstance(drivers_data, list):
            print("No drivers available - skipping race")
            continue

        if not isinstance(results_data, list):
            print("No results available - skipping race")
            continue

        drivers_df = pd.DataFrame(drivers_data)

        results_df = pd.DataFrame(results_data)
        results_df = results_df.rename(
            columns={"position": "finish_position"}
        )

        ####################
        #Merge
        ####################
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
        ####################
        #Data Checks
        ####################
        race_df["finished_in_points"] = (race_df["points"] > 0).astype(int)
    
        
        print("merged here -----")
        print(race_df.head())
        print(race_df.columns)
    
    
    
        race_df["year"] = session["year"]
        race_df["circuit_name"] = session["circuit_short_name"]
        race_df["race_date"] = session["date_start"]
        
        
        all_races.append(race_df)
    
    season_df = pd.concat(
        all_races,
        ignore_index=True
    )
    
    print(season_df)
    
    season_df.to_csv(
        "F1-2023.csv",
        index=False
    )
    # PredictedPosition = 10 # Initial hard-coded value for tests 
    # After qualifying, predict whether a driver will finish in points (TOP 10)
    # driverFinishInPoints = 1 if PredictedPosition <= 10 else 0 # Binary Classification 
        
        
else:
        print("The API returned an error:")
        print(data)

    