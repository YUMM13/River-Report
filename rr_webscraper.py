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

# method responsible for getting the river data
def get_river_data():
    global colorado_basin
    global green_river_basin
    global san_juan_basin
    global great_basin
    global salt_basin
    global verde_basin

    # make a GET response to the website
    rr_website = "https://www.cbrfc.noaa.gov/rec/rec.php"
    response = requests.get(rr_website)

    # parse html content
    soup = BeautifulSoup(response.content, "lxml")

    # get all rr tables from the content
    tables = soup.find_all("table")

    # organize the table into info, basin names, and data

    col = set()
    green = set()
    san_juan = set()
    great = set()
    salt = set()
    verde = set()

    # iterate over all tables
    for t in tables:
        # iterate over each row in the table
        basin_name = ""
        river_name = ""
        flow_rate = ""
        forecast = ""
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
                        river_name = ""
                        flow_rate = ""
                        forecast = ""
                    else:
                        flow_rate = text
                else:
                    forecast = td.text

            # sort the data by basin
            if basin_name == "-Colorado Basin-" and river_name != "" and river_name != None:
                col.add((river_name, flow_rate, forecast))
            elif basin_name == "-Green River Basin-" and river_name != "" and river_name != None:
                green.add((river_name, flow_rate, forecast))
            elif basin_name == "-San Juan Basin-" and river_name != "" and river_name != None:
                san_juan.add((river_name, flow_rate, forecast))
            elif basin_name == "-Great Basin-" and river_name != "" and river_name != None:
                great.add((river_name, flow_rate, forecast))
            elif basin_name == "-Salt Basin-" and river_name != "" and river_name != None:
                salt.add((river_name, flow_rate, forecast))
            else:
                if river_name != None:
                    verde.add((river_name, flow_rate, forecast))
    
    # conver to arrays for ordering and list them
    colorado_basin = list(col)
    green_river_basin = list(green)
    san_juan_basin = list(san_juan)
    great_basin = list(great)
    salt_basin = list(salt)
    verde_basin = list(verde)


def create_table(river_data, frame, ):
    # build table
    river_table = ttk.Treeview(frame)

    # define and format columns
    river_table['columns'] = ('River Name', 'Flow (cfs)', '24 Hour Forecast Trend')
    river_table.column('#0', width=0, stretch='no')
    river_table.column('River Name', anchor='w')
    river_table.column('Flow (cfs)', anchor='w')
    river_table.column('24 Hour Forecast Trend', anchor='w')

    # create headings
    river_table.heading('#0', text='', anchor='w')
    river_table.heading('River Name', text='River Name', anchor='w')
    river_table.heading('Flow (cfs)', text='Flow (cfs)', anchor='w')
    river_table.heading('24 Hour Forecast Trend', text='24 Hour Forecast Trend', anchor='w')

    # add data
    for count, entry in enumerate(river_data, start=1):
        river_table.insert(parent='', index='end', iid=count, text='', values=entry)

    river_table.pack(pady=20)

# ----------------------------------------------------- END OF HELPER METHODS ----------------------------------------------------------

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

# pull data from website
get_river_data()
print(colorado_basin)
# Display data in the table
create_table(colorado_basin, frame)

root.mainloop()