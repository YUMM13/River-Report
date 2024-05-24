import tkinter as tk
from tkinter import ttk

class RiverCardApp:
    def __init__(self, root, rivers):
        self.root = root
        self.root.title("River Cards")
        self.rivers = rivers
        self.index = 0  # To keep track of which rivers are currently displayed

        # Create frames for cards
        self.cards = [self.create_card(i) for i in range(7)]
        
        # Start the update loop
        self.update_cards()
        
    def create_card(self, position):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=position, column=0, padx=10, pady=5, sticky="ew")
        
        card_text = tk.StringVar()
        card_label = ttk.Label(frame, textvariable=card_text, font=('Arial', 16))
        card_label.pack(anchor='w')
        
        return {
            "frame": frame,
            "card_text": card_text,
            "card_label": card_label
        }
    
    def update_cards(self):
        # Update each card with the corresponding river data
        for i, card in enumerate(self.cards):
            river_index = (self.index + i) % len(self.rivers)
            river = self.rivers[river_index]
            card["card_text"].set(f"River: {river['name']}, Flow Rate: {river['flow_rate']}, Forecast: {river['forecast']}")
            
        # Increment index to show next set of rivers in the next update
        self.index = (self.index + 7) % len(self.rivers)
        
        # Call this method again after 5000 milliseconds (5 seconds)
        self.root.after(5000, self.update_cards)
    
    
def main():
    # Example river data
    rivers = [
        {"name": f"River {i+1}", "flow_rate": f"{100+i*10} m^3/s", "forecast": forecast}
        for i, forecast in enumerate(
            ['Sunny', 'Rainy', 'Flood', 'Cloudy'] * 12 + ['Sunny']
        )
    ]

    root = tk.Tk()


    app = RiverCardApp(root, rivers)
    root.mainloop()

if __name__ == "__main__":
    main()
