import re
import requests

import pandas as pd

from bs4 import BeautifulSoup
from datetime import datetime

def get_web_data(url):
    """
    Scrapes web data from a supplied url. This is a simple approach
    that uses the BeautifulSoup html parser. 

    :param String url: Source URL to pull data from.
    :return BeautifulSoup Object: HTML contents of the parsed url.
    """
    # Making a GET request
    try:
        r = requests.get(url)
        
        # check status code for response received
        if r.status_code == 200:
            print(f"...Success pulling data from {url}")
            
    except:
        print("Error in pulling")
        return None
        # print(e)

    # Parsing the HTML 
    soup = BeautifulSoup(r.content, "html.parser")
    return soup

def get_city_names():
    """
    Pulls all available cities that have Costco wait time information.
    Right now we have this as a manually generated list but can 
    convert this in the future to dynamically pull from isitpacked.com.

    :return dict: A dictionary containing the city names and associated 
        URLs.
    """
    city_url_dict = {}
    # For right now, won't get the company names dynamically. There
    # is a radius slider on the website that doesn't allos you to pull
    # for all available Costcos automatically.
    # city_name_soup = get_web_data("https://www.isitpacked.com/place-category/costco/")
    # city_name_list = extract_costco_data(soup, "Get all city names with avialable data")
    
    # Single city name + url for testing
    city_name = "Tampa Bay"
    url = "https://www.isitpacked.com/place/costco-tampa-bay/"
    
    # Dictionary of all available city names from isitpacked.com
    city_name_list = [
        "Costco Orange County, CA",
        "Costco Tampa Bay",
        "Costco Detroit",
        "Costco Portland",
        "Costco Minneapolis-St. Paul",
        "Costco Phoenix",
        "Costco Atlanta",
        "Costco Denver",
        "Costco Seattle-Tacoma",
        "Costco Chicago",
        "Costco Houston",
        "Costco Miami",
        "Costco New York",
        "Costco Inland Empire",
        "Costco Los Angeles",
        "Costco Dallas/Fort Worth",
        "Costco Las Vegas",
        "Costco San Diego"
    ]
    
    # Format the city name for readability and create url for each city
    for city_name in city_name_list:
        city = city_name.replace("Costco ", "")
        
        url_city = re.sub('[^A-Za-z0-9]+', '-', city_name.lower())
        url = f"https://www.isitpacked.com/place/{url_city}/"
        
        city_url_dict[city] = url
        
    return city_url_dict

def extract_costco_data(soup):
    """
    Parses through the pulled soup contents and separates out the 
    necessary data needed for our analysis:
        1. City name
        2. Average wait time within the city
        3. Costco locations within the city
        4. Wait times reported for each location

    :param : BeautifulSoup Object soup: HTML contents of the parsed url.
    :return dict: dictionary containing the above information. Location
        names and wait times are in dict format.
    """
    # Parse through soup object to get the required live data
    city_name_soup = soup.find("div", class_="rpt_plan").find("div", class_="rpt_recurrence")
    city_name = city_name_soup.find("strong").get_text()

    city_avg_wait = soup.find("div", class_="rpt_price").get_text()

    location_avg_wait = soup.find("table")
    
    city_locations_dict = {}

    # Convert html table of average wait per location to Python dict
    for row in location_avg_wait.find_all("tr"):
        col = row.find_all("td")
        if len(col) > 0:
            try:
                key = col[0].contents[0]
                value = col[1].contents[0]
                
                city_locations_dict[key] = value
            
            except IndexError:
                if len(col[0].contents) > 0 or len(col[1].contents) > 0:
                    print("IndexError: Couldn't pull any values for this row")
                    print(col)
                # Else, the col variable was empty 
                    # not an error, just no more location data for this city
                    # col[0].contents or col[1].contents are an empty list []
    
    costco_city_info_dict = {"city_name": city_name,
                             "city_avg_wait": city_avg_wait,
                             "city_locations_info": city_locations_dict}
    
    return costco_city_info_dict
    
def costco_data_cleanup(costco_wait_times_list):
    """
    Create a pandas dataframe out of the initial costco info dictionary
    for easier downstream use/analysis. 
    
    :param list costco_wait_times_list: List of all Costco city info
        dictionaries. [{city1 information}, {city2 information}, ...]
    :return Pandas DataFrame: cleaned dataframe of the following 
        structure:
            city_name         object
            city_avg_wait      int64
            store_location    object
            location_wait      int64
    """
    temp_costco_df = pd.DataFrame.from_dict(costco_wait_times_list)
    
    # We need to explode out the dictionary in the city_locations_info 
    # column to be able to use the more specific locatino data.
    store_location_df = pd.DataFrame([*temp_costco_df['city_locations_info']],temp_costco_df.index).stack().\
        rename_axis([None,'store_location']).reset_index(1, name='location_wait')
        
    costco_cleaned_df = temp_costco_df[['city_name', 'city_avg_wait']].join(store_location_df).reset_index(drop=True)
    
    # Convert the wait times from String "xmin" to int x
    for col_name in ['city_avg_wait', 'location_wait']:
        costco_cleaned_df[col_name] = costco_cleaned_df[col_name].str.replace("min", "").astype(int)
    
    return costco_cleaned_df

def main():
    """
    Driver function. Once completed, data is saved to a csv with the 
    time run as the indentifying key.
    """
    current_time = datetime.now().isoformat(' ', 'minutes')
    costco_wait_times_list = []
    
    city_url_dict = get_city_names()
    
    for city_name, url in city_url_dict.items():
        print(f"Pulling Costco wait time data for   {city_name}   as of {current_time}...")
    
        soup = get_web_data(url)

        # Continue if data exists for URL
        if soup:
            costco_city_info_dict = extract_costco_data(soup)
            
            costco_wait_times_list.append(costco_city_info_dict)
        else:
            print("There was an error pulling website data. Nothing to parse.")
    
    # Data cleanup and convert to pandas df [:-3]
    print(f"Finished pulling all city data. There is data available for {len(costco_wait_times_list)} cities.")
    
    costco_cleaned_df = costco_data_cleanup(costco_wait_times_list)
    print(f"Final DF dtypes: {costco_cleaned_df.dtypes}")
    
    # Save to csv
    current_time_csv_tag = re.sub('[^A-Za-z0-9]+', '_', current_time)
    costco_cleaned_df.to_csv(f"Costco_Wait_Times_US_{current_time_csv_tag}.csv")
    
main()