from bs4 import BeautifulSoup
import requests
import json
import customtkinter as ctk

# globals used for storing basin info
colorado_basin = []
green_river_basin = []
san_juan_basin = []
great_basin = []
salt_basin = []
verde_basin = []

# method responsible for getting the river data
def get_river_data():
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
    forecast = ""

    # iterate over all tables
    # with open('data.json', 'w') as file:
    for t in tables:
        # iterate over each row in the table
        for r in t.find_all("tr"):
            for td in r.find_all("td"):
                # get the river names
                if td.find('a'):
                    river_name = td.a.text.strip()
                # get the basin names and flow rates
                elif td.find('b'):
                    text = td.b.text.strip()
                    if text[0] == '-':
                        basin_name = text
                    else:
                        flow_rate = text
                else:
                    forecast = td.text

            # sort the data by basin
            if basin_name == "-Colorado Basin-" and river_name != "":
                colorado_basin.append((river_name, flow_rate, forecast))
            elif basin_name == "-Green River Basin-" and river_name != "":
                green_river_basin.append((river_name, flow_rate, forecast))
            elif basin_name == "-San Juan Basin-" and river_name != "":
                san_juan_basin.append((river_name, flow_rate, forecast))
            elif basin_name == "-Great Basin-" and river_name != "":
                great_basin.append((river_name, flow_rate, forecast))
            elif basin_name == "-Salt Basin-" and river_name != "":
                salt_basin.append((river_name, flow_rate, forecast))
            else:
                verde_basin.append((river_name, flow_rate, forecast))
    
    print(colorado_basin)


# set color theme for gui
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

# creates main window
root = ctk.CTk()
root.geometry("720x720")

# this is where all of our stuff will go
frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = ctk.CTkLabel(master=frame, text="test")
label.pack(pady=12, padx=10)

get_river_data()

# # Display data in the table
# for row, item in enumerate(colorado_basin, start=1):
#     for col, value in enumerate(item):
#         ctk.CTkLabel(frame, text=value).grid(row=row, column=col)

root.mainloop()