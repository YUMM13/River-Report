from bs4 import BeautifulSoup
import requests
import customtkinter as ctk
from tkinter import ttk

class WebScraper:
    def __init__(self):
        # globals used for storing basin info
        # self.colorado_basin = []
        # self.green_river_basin = []
        # self.san_juan_basin = []
        # self.great_basin = []
        # self.salt_basin = []
        # self.verde_basin = []

        self.rivers = set()

    # def get_col(self):
    #     return self.colorado_basin
    
    # def get_green_river(self):
    #     return self.
    
    # def get_san_juan(self):
    #     return self.colorado_basin
    
    # def get_great(self):
    #     return self.colorado_basin
    
    # def get_salt(self):
    #     return self.colorado_basin
    
    # def get_verde(self):
    #     return self.colorado_basin
    
    # def get_rivers(self):
    #     return self.rivers

    # insertion sort method taken from Geeks for Geeks: https://www.geeksforgeeks.org/python-program-for-insertion-sort/
    # modified to sort based on the name of the basin, if two rivers are in the same basin, then they are compared using
    # their river names
    def insertion_sort(self):
        sorted_arr = list(self.rivers)
        n = len(sorted_arr)  # Get the length of the array
        
        if n <= 1:
            return  # If the array has 0 or 1 element, it is already sorted, so return
    
        for i in range(1, n):  # Iterate over the array starting from the second element
            key = sorted_arr[i]  # Store the current element as the key to be inserted in the right position
            j = i-1
            while j >= 0 and (key[0] < sorted_arr[j][0] or (key[0] == sorted_arr[j][0] and key[1] < sorted_arr[j][1])):  # Move elements greater than key one position ahead
                sorted_arr[j+1] = sorted_arr[j]  # Shift elements to the right
                j -= 1
            sorted_arr[j+1] = key  # Insert the key in the correct position
        
        return sorted_arr

    # method responsible for getting the river data
    def get_river_data(self):
        # make a GET response to the website
        rr_website = "https://www.cbrfc.noaa.gov/rec/rec.php"
        response = requests.get(rr_website)

        # parse html content
        soup = BeautifulSoup(response.content, "lxml")

        # get all rr tables from the content
        tables = soup.find_all("table")

        # organize the table into info, basin names, and data
        # col = set()
        # green = set()
        # san_juan = set()
        # great = set()
        # salt = set()
        # verde = set()
        # river_set = set()

        # clear the rivers set for any new updates
        self.rivers.clear()

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
                            basin_name = text.strip('-')
                            river_name = ""
                            flow_rate = ""
                            forecast = ""
                        else:
                            flow_rate = text
                    else:
                        forecast = td.text

                # sort the data by basin
                # if basin_name == "-Colorado Basin-" and river_name != "" and river_name != None:
                #     col.add((river_name, flow_rate, forecast))
                # elif basin_name == "-Green River Basin-" and river_name != "" and river_name != None:
                #     green.add((river_name, flow_rate, forecast))
                # elif basin_name == "-San Juan Basin-" and river_name != "" and river_name != None:
                #     san_juan.add((river_name, flow_rate, forecast))
                # elif basin_name == "-Great Basin-" and river_name != "" and river_name != None:
                #     great.add((river_name, flow_rate, forecast))
                # elif basin_name == "-Salt Basin-" and river_name != "" and river_name != None:
                #     salt.add((river_name, flow_rate, forecast))
                # else:
                #     if river_name != None:
                #         verde.add((river_name, flow_rate, forecast))

                if river_name != "" and river_name != None:
                    self.rivers.add((basin_name, river_name, flow_rate, forecast))
        
        # conver to arrays for ordering and list them
        # self.colorado_basin = self.insertion_sort(col)
        # self.green_river_basin = self.insertion_sort(green)
        # self.san_juan_basin = self.insertion_sort(san_juan)
        # self.great_basin = self.insertion_sort(great)
        # self.salt_basin = self.insertion_sort(salt)
        # self.verde_basin = self.insertion_sort(verde)

        return self.insertion_sort()


def create_table(river_data, frame):
    # build table
    river_table = ttk.Treeview(frame)

    # define and format columns
    river_table['columns'] = ('Basin Name', 'River Name', 'Flow (cfs)', '24 Hour Forecast Trend')
    river_table.column('#0', width=0, stretch='no')
    river_table.column('Basin Name', anchor='w')
    river_table.column('River Name', anchor='w')
    river_table.column('Flow (cfs)', anchor='w')
    river_table.column('24 Hour Forecast Trend', anchor='w')

    # create headings
    river_table.heading('#0', text='', anchor='w')
    river_table.heading('Basin Name', text='River Name', anchor='w')
    river_table.heading('River Name', text='River Name', anchor='w')
    river_table.heading('Flow (cfs)', text='Flow (cfs)', anchor='w')
    river_table.heading('24 Hour Forecast Trend', text='24 Hour Forecast Trend', anchor='w')

    # add data
    for count, entry in enumerate(river_data, start=1):
        river_table.insert(parent='', index='end', iid=count, text='', values=entry)

    river_table.pack(pady=20)

# ----------------------------------------------------- END OF HELPER METHODS ----------------------------------------------------------

# # set color theme for gui
# ctk.set_appearance_mode("light")
# ctk.set_default_color_theme("dark-blue")

# # creates main window
# root = ctk.CTk()
# root.geometry("720x720")

# # this is where all of our stuff will go
# frame = ctk.CTkFrame(master=root)
# frame.pack(pady=20, padx=60, fill="both", expand=True)

# label = ctk.CTkLabel(master=frame, text="test")
# label.pack(pady=12, padx=10)

# # pull data from website
# ws = WebScraper()
# data = ws.get_river_data()

# # Display data in the table
# create_table(data, frame)

# root.mainloop()