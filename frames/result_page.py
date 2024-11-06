from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from votingsystem.test.voting_system import VotingSystem
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ResultPage:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app

        self.vote = VotingSystem()

        # Create a frame to hold the register page content
        self.parent_frame = ttk.Frame(self.parent, padding=(10, 10))
        
        # Create a canvas to display the background image
        self.bg_canvas = Canvas(self.parent_frame)
        self.bg_canvas.place(relheight=1, relwidth=1)  # Make canvas fill the entire window

        # Load the image
        self.bg_image = Image.open("./assets/img/landing_page.png")  # Ensure the path is correct

        # Bind the resize event to the function on the parent
        self.parent_frame.bind("<Configure>", self.resize_image)

        # Create a frame for the plot
        self.plot_frame = ttk.Frame(self.parent_frame)
        self.plot_frame.pack(fill=BOTH, expand=True)

        # Create a label for displaying the vote numbers
        self.vote_label = ttk.Label(self.parent_frame, text="Click 'Show Results' button to see resuls", font=("Arial", 12), background="white")
        self.vote_label.pack(pady=10)

        # Create custom styles for buttons
        self.style = ttk.Style()
        self.style.configure("Font.TButton", 
                             font=("Arial", 12), 
                             padding=6,
                             background="green", 
                             foreground="white"
                             )  # Customize font and padding for Proceed button

        # Add a button to display results
        self.show_results_button = ttk.Button(self.parent_frame, text="Show Results", style="Font.TButton", command=self.display_results)
        self.show_results_button.pack(pady=20)

        # Back to home button
        self.back_button = ttk.Button(self.parent_frame, text="Back to Home", style="Font.TButton", command=self.on_back)
        self.back_button.pack(pady=10)

    def resize_image(self, event):
        # Get the size of the window
        new_width = event.width
        new_height = event.height

        # Resize the image to the new window size
        resized_image = self.bg_image.resize((new_width, new_height), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(resized_image)

        # Update the canvas with the resized image
        self.bg_canvas.create_image(0, 0, image=bg_photo, anchor=NW)

        # Store a reference to the image to avoid garbage collection
        self.bg_canvas.bg_photo = bg_photo

    def display_results(self):
        results = self.vote.get_results()  # Assuming this returns your result data

        # Extract candidate names and vote counts
        candidate_names = [f"{candidate[1]} ({candidate[0]})" for candidate in results]
        votes = [candidate[2] for candidate in results]

        # Create a figure for the line graph
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.plot(candidate_names, votes, marker='o', linestyle='-', color='green')

        # Set labels and title
        ax.set_title('Voting Results')
        ax.set_xlabel('Candidates')
        ax.set_ylabel('Number of Votes')
        ax.set_ylim(0, max(votes) + 1)  # Set y-axis limit slightly above max votes for better visibility
        ax.grid(True)

        # Embed the plot in the Tkinter frame
        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=BOTH, expand=True)

        # Update the vote label with vote counts
        vote_summary = "\n".join([f"{candidate[1]} ({candidate[0]}): {candidate[2]} votes" for candidate in results])
        self.vote_label.config(text=vote_summary)  # Update the label with the vote summary

    def on_back(self):
        self.app.show_landing_page()  # Switch back to the landing page

    def show(self):
        self.parent_frame.pack(fill="both", expand=True, anchor=CENTER) 

    def hide(self):
        self.parent_frame.pack_forget()

