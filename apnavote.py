# main.py
from tkinter import *
import tkinter as tk

# Import the page classes
from frames.landing_page import LandingPage  
from frames.register_page import RegisterPage
from frames.result_page import ResultPage  # Import the ResultPage
from frames.voting_page import VotingPage

class ApnaVoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ApnaVote")

        # Bind keys for fullscreen functionality
        self.root.bind("<F11>", self.toggle_fullscreen)  # Press F11 to toggle fullscreen
        self.root.bind("<Escape>", self.end_fullscreen)   # Press Escape to exit fullscreen

        # Make the window fullscreen
        self.root.attributes("-fullscreen", True)

        # Initialize pages
        self.landing_page = LandingPage(self.root, self)
        self.register_page = RegisterPage(self.root, self)
        self.voting_page = VotingPage(self.root, self)
        self.result_page = ResultPage(self.root, self)  # Initialize ResultPage

        # Show the landing page initially
        self.show_landing_page()

    def show_landing_page(self):
        """Display the landing page and hide other pages."""
        self.register_page.hide()
        self.voting_page.hide()
        self.result_page.hide()
        self.landing_page.show()

    def show_register_page(self):

        """Display the register page and hide other pages."""
        self.landing_page.hide()
        self.voting_page.hide()
        self.result_page.hide()
        self.register_page.show()

    def show_voter_page(self):
        """Display the voting page and hide other pages."""
        self.register_page.hide()
        self.landing_page.hide()
        self.result_page.hide()
        self.voting_page.show()

    def show_result_page(self):
        """Display the result page and hide other pages."""
        self.register_page.hide()
        self.voting_page.hide()
        self.landing_page.hide()
        self.result_page.show()

    # Function to toggle fullscreen
    def toggle_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))

    # Function to exit fullscreen
    def end_fullscreen(self, event=None):
        self.root.destroy()

# Create main root window
if __name__ == "__main__":
    root = tk.Tk()
    app = ApnaVoteApp(root)  # Create an instance of the ApnaVoteApp class
    root.mainloop()  # Run the main loop
