import tkinter as tk
import colorama
from minspec import MinSpec
from recspec import RecSpec

colorama.init(autoreset=True)

"""
This program provides a GUI application that allows users to compare their system specifications against
the minimum and recommended system requirements for various video games and applications. 
Users can select a video game or application from a dropdown menu and then click the corresponding button to 
display either the minimum or recommended system requirements for their selection.

The Systemreq class is a tkinter-based GUI application that displays the main window and handles user input.
It initializes MinSpec and RecSpec objects for managing minimum and recommended system requirements, respectively.
The class provides methods to handle user interactions, such as selecting a game or application from the dropdown
menu and updating the displayed system requirements.
"""


# Main app class, inheriting from tkinter.Tk
class Systemreq(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("System Requirements Simulator")
        self.geometry("800x400")
        self.config(bg='grey')

        # Mapping between selection names and application IDs
        self.selection_to_app_id = {
            "------Video Games------": "",
            "Elden Ring": 12,
            "FIFA 23": 13,
            "God of War": 9,
            "Grand Theft Auto V": 7,
            "Microsoft Flight Simulator": 10,
            "Minecraft": 5,
            "The Sims 4": 8,
            "------Applications------": "",
            "Adobe Photoshop": 6,
            "Adobe Premiere Pro": 15,
            "Blender": 14
        }

        # Initialize MinSpec and RecSpec objects with the application IDs
        self.minspec = MinSpec(self.selection_to_app_id)
        self.recspec = RecSpec(self.selection_to_app_id)

        # Create a StringVar to track the selected value
        self.click = tk.StringVar()
        self.click.set("Video Games and Applications")

        # Create the OptionMenu with the dropdown selections and set the command to update the minspec/recspec values
        drop = tk.OptionMenu(self, self.click, *self.selection_to_app_id.keys(), command=self.select_games)
        drop.config(bg='green', activebackground='pink')
        drop['menu'].config(bg='green', activebackground='pink')
        drop.pack()

        # Create Minimum Specs and Recommended Specs buttons
        minspec_button = tk.Button(self, text="Minimum Specs", command=self.update_minspec)
        minspec_button.pack()

        recspec_button = tk.Button(self, text="Recommended Specs", command=self.update_recspec)
        recspec_button.pack()
        # Create a text widget to display results
        self.result_text = tk.Text(self, state='disabled', width=400, height=400)
        self.result_text.pack()

        # Run the tkinter main loop
        self.mainloop()

    # Return the selected game or application from the dropdown
    def select_games(self, selection):
        return selection

    # Update the displayed minimum specs based on the selected game or application
    def update_minspec(self):
        select_game = self.click.get()
        self.minspec.update_minspec(select_game, self.result_text)

    # Update the displayed recommended specs based on the selected game or application
    def update_recspec(self):
        select_game = self.click.get()
        self.recspec.update_recspec(select_game, self.result_text)


# Run this as the main program
if __name__ == "__main__":
    app = Systemreq()
