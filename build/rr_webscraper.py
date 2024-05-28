from bs4 import BeautifulSoup
import requests
import customtkinter as ctk
from tkinter import ttk

class WebScraper:
    def __init__(self):
        self.rivers = set()

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

    def get_river_data(self):
        # make a GET response to the website
        rr_website = "https://www.cbrfc.noaa.gov/rec/rec.php"
        response = requests.get(rr_website)

        # parse html content
        soup = BeautifulSoup(response.content, "lxml")

        # get all rr tables from the content
        tables = soup.find_all("table")

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
                
                # do not include headers in the rivers set
                if river_name != "" and river_name != None:
                    self.rivers.add((basin_name, river_name, flow_rate, forecast))
        
        # convert to array and sort it for consistency
        return self.insertion_sort()
