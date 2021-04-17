import os
from dotenv import load_dotenv
import pandas as pd
import requests
import json

load_dotenv()

API_KEY = os.getenv("API_KEY_ACS")
STATE = "06"  # California state geoID
PALM_SPRINGS = "55254"
RANCHO_MIRAGE = "59500"
pop_group = "B01001"

geoids = pd.read_csv("geoids_clean.csv")

# ---------------------------
# THINGS TO DO:
# ---------------------------

# MUST-DO:


def geoid_from_city(city: str):
    """
    Gets the geoid from the city name using the city geocode csv
    
    Argument(s)
    -----------------------
        city: Argument must be in the string format. Example: 
              "Rancho Mirage, CA"
    
    Output
    -----------------------
    Geo ID in string format. Example is Rancho Mirage's Geo ID:
        "59500" 
    """

    temp = geoids[geoids["City"] == city] # Filter out all cities that are not targets
    geoid = list(temp["city_geoid"])[0] # Grab the first result of the corresponding geoID

    return geoid

def city_from_geoid(geoid: str):
    """
    Returns the city associated with a particular geoid.
    
    Argument(s) 
    -----------------------
        geoid:  city geoid (without the state id) in string format. Example: 
                "59500"
    
    Output
    -----------------------
    City name in string format. Example:
        "Rancho Mirage, CA"
    """
    # TODO: fix docstring output 

    temp = geoids[geoids["city_geoid"] == int(geoid)] #Filter out all the geoids that are not tarfers
    city = list(temp["City"])[0] #Grab the first result of the corresponding City
    
    return city

def base_url(year: str):
    """
    Helper function. Returns the base URL for the ACS API for a year
    
    Argument(s) 
    -----------------------
        year:  year of data needed to pull in string format. Example: 
                "2021"
    
    Output
    -----------------------
    base url in string (f string) format. Example:
        https://api.census.gov/data/2021/acs/acs5
    """

    return f"https://api.census.gov/data/{str(year)}/acs/acs5"

def get_population_estimate(year: str, city: str):
    """
    Pulls the population estimate data from ACS for a city and year.
    NOTE: Returns "Connection refused by the server.." if no connection to server

    TODO: This currently doesn't return anything so need to check if function is needed
    
    Argument(s) 
    -----------------------
        year: year of data needed to pull in string format. Example: 
              "2021"
        city: city id in string format. Example is Rancho Mirage: 
              "59500"
    
    Output
    -----------------------
    returns population estimate in List of List of strings format. Example:
        [['NAME', 'B01001_001E', 'state', 'place'], ['Palm Springs city, California', '47897', '06', '55254']] 
    
    """
    pop_est = "B01001_001E"  # according to 2019 variable list
    total_population = base_url(year) + f"?get=NAME,{pop_est}&for=place:{city}&in=state:{STATE}"
    try:
        r = requests.get(total_population)
        print(r.json())
        # [['NAME', 'B01001_001E', 'state', 'place'], ['Palm Springs city, California', '47897', '06', '55254']]
    except:
        print(total_population)
        print("Connection refused by the server..")


def collect_group(group: str, year: str, city: str):
    """
    Pulls the data from ACS with the series id from the group for city and year
    NOTE: Returns "Connection refused by the server.." if no connection to server

    Argument(s)
    -----------------------
        group: Series ID of group you want to pull from in string format Example for SEX BY AGE:
               "B01001"
        year:  year of data needed to pull in string format. Example: 
               "2021"
        city:  city id in string format. Example is Rancho Mirage: 
               "59500" 
        
    Output:
    -----------------------
        List of lists of strings with the series ID in the first list and the value in the second list
        
        Format of List of Lists: 
        list[0] = list of series ids 
            NOTE: at the end of the list it includes "NAME, 'state', 'place'"
        list[1] = list of corresponding values 
            NOTE: at the end of the list it includes the corresponding values to the first list 
                  Example: 'Palm Springs city, California',  '06', '55254'

        Example:
        [['B01001_001E', ... , 'NAME', 'state', 'place'], ['47897', ... , 'Palm Springs city, California',  '06', '55254']]
    """
    temp = base_url(year) + f"?get=group({group})&for=place:{city}&in=state:{STATE}&key={API_KEY}"
    try:
        r = requests.get(temp)
        return r.json()
    except:
        print(temp)
        print("Connection refused by the server..")


# get_population_estimate('2019',PALM_SPRINGS)
# https://github.com/datamade/census
# collect_group(pop_group, "2019", PALM_SPRINGS)

def year_df(group: str, year: str, city: str = PALM_SPRINGS):
    """
    This function allows us to pull any series we want and export it to a human-readable (i.e., column names are in English) dataframe for one year.

    We get series IDs that only end in 'E'

    Argument(s)
    -----------------------
        group: Series ID of group you want to pull from in string format Example for SEX BY AGE:
               "B01001"
        year:  year of data needed to pull in string format. Example: 
               "2021"
        city:  city id in string format. Example is Rancho Mirage: 
               "59500" 
        
    Output:
    -----------------------
    A data frame with two rows, first row has each concept + label as a column and the second row contains its values. The index will be the year.

    """
    # Opens the JSON file
    with open("acs_vars_2019.json") as vars_json:
        varDict = json.load(vars_json) #Load the json file to varDict

    LoL =  collect_group(group, year, city) # Pulls the data from ACS returns a List of List (LoL)

    ids = LoL[0] # list 0 = list of series ids
    vals = LoL[1] #list 1 = list of corresponding values
    
    concept_label = [] #initialise a concept with label list which will be a column
    values = [] #initialse the list of values column of concept with label which will be a column
    
    for i in range(len(ids)):
        if (ids[i]) == 'NAME': #This is when we reached the end of the series ID data we break the loop since we don't want it to run anymore
            break 
        if (ids[i][-1]) == 'E':
            # RENAME THE SERIES HERE
            ser = ids[i] #Get the Series ID from the LoL
            concept_label.append(varDict[ser]["Concept"] + " " + varDict[ser]["Label"]) #combining concept + label from the json file to a single element of the concept label lsit
            values.append(vals[i]) #Adds the value to the values list.
            
    # Create a dataframe for our output
    acs_df = pd.DataFrame({
        # Here are the columns of the dataframe
        "concept_label" : concept_label, 
        "values" : values
        "year" : year
    })

    acs_df = acs_df.pivot(index = "year", columns = "concept_label", values = "values") #Pivot the DF so we can have each concept label as its own column on one row and the values in the row below
    
    return acs_df

def generate_df_city(group: str, start_year: str = '2011', end_year: str = '2019', city: str = PALM_SPRINGS):
    """
    Generates a dataframe for a city's data from ACS, given a start and end year.
    
    Argument(s)
    -----------------------
        group:       Series ID of group you want to pull from in string format Example for SEX BY AGE:
                     "B01001"
        start_year:  year of data needed to pull in string format. Example: 
                     "2011"
                     NOTE: must be 2011 or later       
        end_year:    year of data needed to pull in string format. Example: 
                     "2019"
                     NOTE: must be 2019 or less
        city:        city id in string format. Example is Rancho Mirage: 
                     "59500" 
        
    Output:
    -----------------------
    A dataframe with the following columns: year (index), city (str), and a separate column for each subgroup.
    """

    dfs = []

    cityName = city_from_geoid(city)

    # Use year_df function to get get all the dfs from the start to the end year
    for year in range(int(start_year), int(end_year) + 1): #start and end year INCLUSIVE
        df = year_df(group, str(year), city)
        dfs.append(year_df(group, str(year), city))
    
    result = pd.concat(dfs)

    result["City"] = cityName #Add the city to the df 

    return result

def generate_csv(group: str, start_year: str = '2011', end_year: str = '2019', cities: str = [PALM_SPRINGS], filename: str = None):
    """
    Uses generate_df_city to create one large dataframe that encompasses all data for a particular ACS series.
    If a filename is given, then csv is created
    
    Argument(s)
    -----------------------
        group:       Series ID of group you want to pull from in string format Example for SEX BY AGE:
                     "B01001"
        start_year:  year of data needed to pull in string format. Example: 
                     "2011"
                     NOTE: must be 2011 or later       
        end_year:    year of data needed to pull in string format. Example: 
                     "2019"
                     NOTE: must be 2019 or less
        cities:      Geo IDs for cities you want to pull in List of strings format. Example is Palm Springs and Rancho Mirage: 
                     ["55254", "59500"] 
        filename:    Filename to name the output .csv file. Leave as None (or use default parameter) if you don't want to save a file. ex. "my_acs_data.csv"

    Output
    -----------------------
    A datafame with the same format as generate_df_city, but contains multiple levels for the City variable rather than just one.
    """
    dfs = []

    for city in cities: #generate the df for all cities in list of cities
        df = generate_df_city(group, start_year, end_year, str(city))
        dfs.append(df)

    res = pd.concat(dfs)

    if filename != None:
        res.to_csv(filename, index = True)

    return res


# TESTING
# print(generate_csv(pop_group, start_year="2011", end_year="2019", cities=[PALM_SPRINGS, RANCHO_MIRAGE], filename = "testSet.csv"))
