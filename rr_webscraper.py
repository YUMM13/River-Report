from bs4 import BeautifulSoup
import requests
import json
import customtkinter as ctk
from tkinter import ttk

# globals used for storing basin info
colorado_basin = []
green_river_basin = []
san_juan_basin = []
great_basin = []
salt_basin = []
verde_basin = []

dupe_check = False

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
        global dupe_check

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
                # deals with edge case because this river is mentioned twice
                if river_name == "Colorado at Westwater":
                    if not dupe_check:
                        dupe_check = True
                    else:
                        break
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
    
    # sort arrays for consistency
    colorado_basin.sort()
    green_river_basin.sort()
    san_juan_basin.sort()
    great_basin.sort()
    salt_basin.sort()
    verde_basin.sort()

    
    #print(colorado_basin)


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

# Display data in the table
# for row, item in enumerate(colorado_basin, start=1):
#     for col, value in enumerate(item):
#         ctk.CTkLabel(frame, text=value).grid(row=row, column=col)

# build table
river_table = ttk.Treeview(frame)

# define and format columns
river_table['columns'] = ('River Name', 'Flow (cfs)', '24 Hour Forecast Trend')
river_table.column('#0', width=0)
river_table.column('River Name', anchor='w')
river_table.column('Flow (cfs)', anchor='w')
river_table.column('24 Hour Forecast Trend', anchor='w')

# create headings
river_table.heading('#0', text='label', anchor='w')
river_table.heading('River Name', text='River Name', anchor='w')
river_table.heading('Flow (cfs)', text='Flow (cfs)', anchor='w')
river_table.heading('24 Hour Forecast Trend', text='24 Hour Forecast Trend', anchor='w')

# add data
for count, entry in enumerate(colorado_basin, start=1):
    river_table.insert(parent='', index='end', iid=count, text='', values=(entry[0], entry[1], entry[2]))

river_table.pack(pady=20)

root.mainloop()