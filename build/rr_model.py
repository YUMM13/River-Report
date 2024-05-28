import datetime as dt
from rr_webscraper import WebScraper

class Model:
    def __init__(self, placeholders, window, canvas):
        # get the text into an array
        self.river_cards = [
            { "basin":placeholders[0],  "river":placeholders[1],  "flow":placeholders[2],  "forecast":placeholders[3],  "box":placeholders[4] },
            { "basin":placeholders[5],  "river":placeholders[6],  "flow":placeholders[7],  "forecast":placeholders[8],  "box":placeholders[9] },
            { "basin":placeholders[10], "river":placeholders[11], "flow":placeholders[12], "forecast":placeholders[13], "box":placeholders[14] },
            { "basin":placeholders[15], "river":placeholders[16], "flow":placeholders[17], "forecast":placeholders[18], "box":placeholders[19] },
            { "basin":placeholders[20], "river":placeholders[21], "flow":placeholders[22], "forecast":placeholders[23], "box":placeholders[24] },
            { "basin":placeholders[25], "river":placeholders[26], "flow":placeholders[27], "forecast":placeholders[28], "box":placeholders[29] }
        ]

        self.win = window
        self.can = canvas
        self.river_index = 0

        # get web scraper obj
        self.ws = WebScraper()

        # get river data from server
        self.river_data = self.ws.get_river_data()

    # helper method that brings in data using the web scraper class
    def refresh_data(self, id):
        # get river data from server
        self.river_data = self.ws.get_river_data()

        # update the time var to show when data was last refreshed
        self.can.itemconfig(tagOrId=id, text=dt.datetime.now().strftime("%I:%M %p"))

    def update_river_cards(self):
        riv_len = len(self.river_data)

        # loop through array and update info based off of info in card
        for i, c in enumerate(self.river_cards):
            index = (self.river_index + i) % riv_len
            river = self.river_data[index]
            self.can.itemconfig(tagOrId=c["basin"],    text=river[0])
            self.can.itemconfig(tagOrId=c["river"],    text=river[1])
            self.can.itemconfig(tagOrId=c["flow"],     text=river[2])
            self.can.itemconfig(tagOrId=c["forecast"], text=river[3])

            # change box color based on forecast
            if "Rise" in river[3]:
                self.can.itemconfig(tagOrId=c["box"], fill="#81e888")
            elif "Fall" in river[3]:
                self.can.itemconfig(tagOrId=c["box"], fill="#e88781")
            elif "Power Release" in river[3]:
                self.can.itemconfig(tagOrId=c["box"], fill="#81b6e8")
            elif "Regulated" in river[3]:
                self.can.itemconfig(tagOrId=c["box"], fill="#e2e881")
            else:
                self.can.itemconfig(tagOrId=c["box"], fill="#A1A1A1")


        # increment river_index to show next set of rivers in next update
        self.river_index = (self.river_index + 7) % riv_len

        # call this method again after 5 seconds
        self.win.after(7000, self.update_river_cards)
