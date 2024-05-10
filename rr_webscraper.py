from bs4 import BeautifulSoup
import requests
import json

# make a GET response to the website
rr_website = "https://www.cbrfc.noaa.gov/rec/rec.php"
response = requests.get(rr_website)

# parse html content
soup = BeautifulSoup(response.content, "lxml")

# get all rr tables from the content
tables = soup.find_all("table")

# organize the table into info, basin names, and data
basin_name = ""
river_name = ""
flow_rate = ""
forecasts = ""
rows = []

# iterate over all tables
with open('data.json', 'w') as file:
    for t in tables:
        # iterate over each row in the table
        for r in t.find_all("tr"):
            # get the river names
            if r.find('a'):
                river_name = r.a.text.strip()
            # get the basin names and flow rates
            if r.find('b'):
                text = r.b.text.strip()
                if text[0] == '-':
                    basin_name = text
                else:
                    flow_rate = text
        
        # turn the data into json
        row = {
            "basin": basin_name,
            "river": river_name,
            "flow": flow_rate
        }
        rows.append(row)

    json.dump(rows, file)


