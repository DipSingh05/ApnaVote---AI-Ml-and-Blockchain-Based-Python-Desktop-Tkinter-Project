# landing_page.py
from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk

class LandingPage:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app

        # Create a frame to hold the register page content
        self.parent_frame = ttk.Frame(self.parent, padding=(10, 10))

        # Create a canvas to display the background image
        self.canvas = Canvas(self.parent_frame)
        self.canvas.place(relheight=1, relwidth=1)  # Make canvas fill the entire window

        # Load the image
        self.bg_image = Image.open("./assets/img/landing_page.png")  # Ensure the path is correct

        # Bind the resize event to the function on the parent
        self.parent_frame.bind("<Configure>", self.resize_image)

        # Create custom styles for buttons
        self.style = ttk.Style()
        self.style.configure("Font.TButton", 
                             font=("Arial", 12), 
                             padding=6,
                             background="green", 
                             foreground="white"
                             )  # Customize font and padding for Proceed button

        # Create and place widgets
        self.proceed_button = ttk.Button(self.parent_frame, text="Proceed", padding=(10, 10), style="Font.TButton", command=self.on_proceed)
        self.register_button = ttk.Button(self.parent_frame, text="Register", padding=(10, 10), style="Font.TButton", command=self.on_register)
        self.result_button = ttk.Button(self.parent_frame, text="View Results", padding=(10, 10), style="Font.TButton", command=self.on_view_results)

        self.label = ttk.Label(self.parent_frame, text="Note: It's a dummy database, replicating Indian citizen criteria. If you are new, register yourself first.", font=("Arial", 10))

        # Initial placement of widgets
        self.proceed_button.place(x=560, y=700)
        self.register_button.place(x=860, y=700)
        self.result_button.place(x=710, y=700)  # Adjust the x position to fit with other buttons
        self.label.place(x=460, y=800)

    def resize_image(self, event):
        # Get the size of the window
        new_width = event.width
        new_height = event.height

        # Resize the image to the new window size
        resized_image = self.bg_image.resize((new_width, new_height), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(resized_image)

        # Update the canvas with the resized image
        self.canvas.create_image(0, 0, image=bg_photo, anchor=NW)

        # Store a reference to the image to avoid garbage collection
        self.canvas.bg_photo = bg_photo

    def on_proceed(self):
        self.app.show_voter_page()

    def on_register(self):
        self.app.show_register_page()  # Switch to register page

    def on_view_results(self):
        self.app.show_result_page()  # Switch to the result page

    def show(self):
        self.parent_frame.pack(fill="both", expand=True, anchor=CENTER) 

    def hide(self):
        self.parent_frame.pack_forget()
