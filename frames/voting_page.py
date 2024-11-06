# voting_page.py
import random
from sre_parse import State
from tracemalloc import start
import cv2
from tkinter import *
from tkinter import filedialog, Toplevel, messagebox
from datetime import datetime, timedelta
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import numpy as np
import json
import random
import time
import re
import os
import base64
import  requests
from io import BytesIO
from fingerprint_manager import FingerprintManager
from firebase_manager import FirebaseDB
from facial_recognition import HeadMovementVerification
from secure import EncryptHash
from send_sms import SendSMS
from votingsystem.test.voting_system import VotingSystem

class VotingPage:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app

        # values
        self.checkbox_var = ttk.BooleanVar()

        # Initialize the live video capture
        self.cap = None
       
          # Initialize variables
        self.selected_candidate = ttk.StringVar()
        self.fraud_count_var = ttk.IntVar(value=0)
        self.countdown_var = ttk.IntVar(value=30)  # Example countdown value
        self.checkpoints = {}
        self.ref_var = False
        self.start_timer = False
        self.is_end = False


        #Initilized fingureprint manager
        self.fp_manager = FingerprintManager()
        self.fp_manager.open_session()  

        #Initilized
        self.db = FirebaseDB()
        self.eh = EncryptHash()
        self.sms = SendSMS()
        self.facial_verify = HeadMovementVerification()
        self.vote = VotingSystem()
        
        # Create a frame to hold the register page content
        self.parent_frame = ttk.Frame(self.parent, padding=(10,10))

        # Create a canvas to display the background image
        self.canvas = Canvas(self.parent_frame)
        self.canvas.place(relheight=1, relwidth=1) # Make canvas fill the entire window

        # Load the image
        self.bg_image = Image.open("./assets/img/background_templete.png")  # Ensure the path is correct

        # Bind the resize event to the function on the parent
        self.parent_frame.bind("<Configure>", self.resize_image)

    # Create custom styles for buttons
        self.style = ttk.Style()
        self.style.configure("Submit.TButton",
                             font=("Arial", 10),
                             padding=4,
                             foreground="white")

        # Header label for the form
        self.header_label = ttk.Label(self.parent_frame, text="Voting Panel!", font=("Arial", 20), width=50,
                                      background='green', foreground="white", padding=10, anchor='center')
        self.header_label.place(relx=0.5, rely=0.08, anchor=CENTER)

        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.parent_frame, padding=(10,10))
        self.notebook.place(relx=0.5, rely=0.56, anchor=CENTER)

        # Create each tab frame
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)
        self.tab4 = ttk.Frame(self.notebook)

        # Add tabs to the notebook
        self.notebook.add(self.tab1, text="Aadhar Auth")
        self.notebook.add(self.tab2, text="Verify & Concern")
        self.notebook.add(self.tab3, text="Fingerprint verify")
        self.notebook.add(self.tab4, text="Give your VOTE")

        # --- TAB 1: Aadhar Auth Form ---
        self.create_tab1()
        
    def create_tab1(self):
        # Frame for form elements
        self.form_frame1 = ttk.Frame(self.tab1)
        self.form_frame1.pack(padx=20, pady=20)

        # Create label and entry for "Aadhar ID"
        self.adhar_label = ttk.Label(self.form_frame1, text="Aadhar ID:", font=("Arial", 14))
        self.adhar_entry = ttk.Entry(self.form_frame1, font=("Arial", 10))
        self.adhar_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.adhar_entry.grid(row=0, column=1, padx=10, pady=10, sticky=W)

        # Send OTP button centered below Aadhar ID entry
        self.otp_button = ttk.Button(self.form_frame1, text="Send OTP", style="Submit.TButton", padding=(10, 10), command=self.fetch_aadhar)
        self.otp_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Create label and entry for "OTP"
        self.otp_label = ttk.Label(self.form_frame1, text="OTP:", font=("Arial", 14))
        self.otp_entry = ttk.Entry(self.form_frame1, font=("Arial", 10))
        self.otp_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)
        self.otp_entry.grid(row=2, column=1, padx=10, pady=10, sticky=W)

        # Verify OTP and Proceed buttons aligned in one row, centered
        button_frame = ttk.Frame(self.form_frame1)  # Create a frame to hold both buttons for better alignment
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        self.verify_otp_button = ttk.Button(button_frame, text="Verify OTP", style="Submit.TButton", padding=(10, 10), state=DISABLED, command=self.verify_otp)
        self.verify_otp_button.grid(row=0, column=0, padx=5)

        self.proceed_button = ttk.Button(button_frame, text="Proceed", style="Submit.TButton", padding=(10, 10), state=DISABLED, command=self.submit_tab1)
        self.proceed_button.grid(row=0, column=1, padx=5)


    def fetch_aadhar(self):
        # Fetch user data
        user_id = self.adhar_entry.get()  # Replace with actual user ID

        if user_id:
            if user_id.isdigit() and len(user_id) == 12:
                has_voted = self.vote.has_voted(user_id)
                print("has-->", has_voted)
                if has_voted == False:
                    self.fetch_user = self.db.fetch_user(user_id)
                    if self.fetch_user:
                        is_link = bool(self.eh.decrypt_data(self.fetch_user['is_linked']))
                        if is_link:
                            number = self.eh.decrypt_data(self.fetch_user['phone'])
                            self.onetimepass = int(''.join([str(random.randint(0, 9)) for _ in range(4)]))
                           
                            sms_result = self.sms.send_sms(
                                body=f"Welcome to APNAVOTE. Your otp is {self.onetimepass}.\n\n # MAIN BHARAT HA. HUM BHARAT KA MATDATA HA..",
                                phone=number
                                )

                            sms_result = True

                            if sms_result:
                                self.verify_otp_button.config(state='normal')
                                self.otp_button.config(state=DISABLED)
                            else:
                                messagebox.showerror('Server Error', f"OTP not send on +91-{number}")
                        else:
                            messagebox.showerror('Error', 'Your voter is not link with aadhar. Link it fast.\n this window will close with in 10 second automatically')
                            time.sleep(10)
                            self.app.destroy()
                    else:
                        messagebox.showerror('Error', f"User with ID {user_id} not found.")
                else:
                    messagebox.showerror("Error", "You already voted!")
            else:
                messagebox.showerror("Error", "Aadhaar ID must be exactly 12 numeric characters.")
        else:
            messagebox.showerror("Error", "All fields must be filled.")

        

    def verify_otp(self):
        if int(self.otp_entry.get()) == self.onetimepass:
            self.decrypted_data_dict = {key: self.eh.decrypt_data(value) for key, value in self.fetch_user.items()}

            # Download the encrypted .bin file
            self.datetime_filename = f"encrypted_images/{self.decrypted_data_dict['datetime']}.bin"
            self.local_bin_path = f"./assets/face/bin/{self.decrypted_data_dict['datetime']}.bin"
            self.local_png_path = f"./assets/face/bin/{self.decrypted_data_dict['datetime']}.png"

            # Download the file
            if self.db.download_image(self.datetime_filename, self.local_bin_path):
                # Convert .bin to .png by decoding the binary data
                try:
                    with open(self.local_bin_path, 'rb') as bin_file:
                        encrypted_data = bin_file.read()  # Read as bytes
                        image_data = self.eh.decrypt_data(encrypted_data)  # Decrypt the binary data

                    if image_data is not None:
                        # Save the decrypted data as a .png file
                        with open(self.local_png_path, 'wb') as png_file:
                            png_file.write(image_data)
                            self.proceed_button.config(state='normal')
                            self.verify_otp_button.config(state=DISABLED)
                    else:
                        messagebox.showerror('Server Error', "Failed to decrypt the image data.")
                except Exception as e:
                    messagebox.showerror('Server Error', f"Error converting .bin to .png: {e}")

    
    def create_tab2(self):
        # Create the main frame for the summary in Tab 4
        self.form_frame2 = ttk.Frame(self.tab2)
        self.form_frame2.pack(padx=10, pady=10)

        self.photo = ImageTk.PhotoImage(Image.open(self.local_png_path))

        # Display Photo
        photo_frame = ttk.LabelFrame(self.form_frame2, text="Photo", padding=(10,10), bootstyle="success")
        photo_frame.grid(row=0, column=0, rowspan=4, columnspan=2, sticky="ew", padx=5, pady=5)

        # Assuming self.photo has been previously loaded with the image
        photo_label = ttk.Label(photo_frame, image=self.photo)
        photo_label.grid(row=0, column=0, padx=2, pady=2)

        # Name Fields
        name_frame = ttk.LabelFrame(self.form_frame2, text="Name Information", padding=(10,10), bootstyle="success")
        name_frame.grid(row=0, column=3, sticky="ew", padx=5, pady=5)
        ttk.Label(name_frame, text=f"First Name: {self.decrypted_data_dict['first_name']}").grid(row=0, column=0, sticky="w", padx=2, pady=2)
        ttk.Label(name_frame, text=f"Last Name: {self.decrypted_data_dict['last_name']}").grid(row=0, column=1, sticky="w", padx=2, pady=2)

         # Aadhaar and Voter IDs
        id_frame = ttk.LabelFrame(self.form_frame2, text="ID Information", padding=(10,10), bootstyle="success")
        id_frame.grid(row=1, column=3, sticky="ew", padx=5, pady=5)
        ttk.Label(id_frame, text=f"Aadhaar ID: {self.decrypted_data_dict['aadhar_id']}").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        ttk.Label(id_frame, text=f"Voter ID: {self.decrypted_data_dict['voter_id']}").grid(row=0, column=1, sticky="w", padx=5, pady=2)
    
        # Personal Information (DOB, Gender)
        personal_frame = ttk.LabelFrame(self.form_frame2, text="Personal Information", padding=(10,10), bootstyle="success")
        personal_frame.grid(row=2, column=3, sticky="ew", padx=5, pady=5)
        ttk.Label(personal_frame, text=f"Date of Birth: {self.decrypted_data_dict['dob']}").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        ttk.Label(personal_frame, text=f"Gender: {self.decrypted_data_dict['gender']}").grid(row=0, column=1, sticky="w", padx=5, pady=2)

        # Linkage and Fingerprint Status Frame
        status_frame = ttk.LabelFrame(self.form_frame2, text="Status Information", padding=(10,10), bootstyle="success")
        status_frame.grid(row=3, column=3, sticky="ew", padx=5, pady=5)
        ttk.Label(status_frame, text=f"Linked to Aadhaar: {self.decrypted_data_dict['is_linked']}").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        ttk.Label(status_frame, text=f"Fingerprint: Captured Successfully").grid(row=0, column=1, sticky="w", padx=5, pady=2)

        # Checkbox for confirmation
        self.checkbox = ttk.Checkbutton(self.form_frame2, text="I, , confirm that the above data mine and it is correct.", variable=self.checkbox_var)
        self.checkbox.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

        # Proceed button
        self.proceed_button = ttk.Button(self.form_frame2, text="Proceed", style="Submit.TButton", command=self.submit_tab2)
        self.proceed_button.grid(row=5, column=3, pady=5, padx=5)


    def create_tab3(self):
        # Label and description for fingerprint capture
        self.fingerprint_label = ttk.Label(self.tab3, text="Capture Fingerprint Here", font=("Arial", 16))
        self.fingerprint_label.pack(pady=20)

        # Frame to hold scan and submit buttons
        button_frame = ttk.Frame(self.tab3)
        button_frame.pack(pady=10)

        # Button to scan fingerprint, triggering the scan window
        self.scan_button = ttk.Button(button_frame, text="Scan Fingerprint", style="Submit.TButton", padding=(10, 10), command=self.open_fingerprint_scan_window)
        self.scan_button.grid(row=0, column=0, padx=10)

        # Button to submit fingerprint data
        self.submit_tab3_button = ttk.Button(button_frame, text="Submit", style="Submit.TButton", padding=(10, 10), command=self.submit_tab3)
        self.submit_tab3_button.grid(row=0, column=1, padx=10)

        # Label to notice
        self.notice_label = ttk.Label(button_frame, text="The fingerprint sensor associated with laptop/mobile can be used for authentication purpose only. Means, you can add the more number of fingerprints who are eligible to access the device. Then, device will allow any one of them to unlock the device. It will not record whose fingerprint it is. It will just say, a fingerprint is authenticated or not.", font=("Arial", 14), wraplength=500)
        self.notice_label.grid(row=1, column=0, columnspan=2, padx=20, pady=40)

        # Label of status
        self.status_label = ttk.Label(self.tab3, text="Click on the scan button", font=("Arial", 12))
        self.status_label.pack(padx=10, pady=10, side="bottom")

    def open_fingerprint_scan_window(self):
        self.status_label.config(text="Place one finger in scanner", foreground="blue")
        self.status_label.update_idletasks()
        stored_fp = self.decrypted_data_dict['fingerprint']
        self.verify_print = self.fp_manager.validate_fingerprint(stored_fp)
        if self.verify_print:
            messagebox.showinfo("Success", "Fingerprint verified successfully.")
            self.status_label.destroy()
            self.fp_manager.close_session()
        else:
            messagebox.showerror("Error", "Fingerprint verified failed.")
            self.status_label.config(text="Click on the scan button", foreground="black")
            self.status_label.update_idletasks()
            self.fp_manager.close_session()
       
        # Enable or disable the submit button based on capture status
        self.scan_button.config(state="disabled" if self.verify_print else "normal")

    def create_tab4(self):
        # Create variables for each Checkbutton
        self.head_up_var = ttk.BooleanVar(value=False)
        self.head_down_var = ttk.BooleanVar(value=False)
        self.head_right_var = ttk.BooleanVar(value=False)
        self.head_left_var = ttk.BooleanVar(value=False)

        # Dictionary for checkbutton labels and associated variables
        self.checkpoints = {
            "Head Up": self.head_up_var,
            "Head Down": self.head_down_var,
            "Head Right": self.head_right_var,
            "Head Left": self.head_left_var
        }

        # Create the frame for Tab 4 (Give your VOTE)
        self.form_frame4 = ttk.Frame(self.tab4)
        self.form_frame4.pack(padx=20, pady=20)

        # Video verification frame (left side)
        video_frame = ttk.LabelFrame(self.form_frame4, text="Video Verification", padding=(10, 10))
        video_frame.grid(row=0, column=0, rowspan=4, sticky="nsew", padx=5, pady=5)

        # Checkpoints frame (right side)
        self.checkpoints_frame = ttk.LabelFrame(self.form_frame4, text="Checkpoints", padding=(10, 10))
        self.checkpoints_frame.grid(row=0, column=1, rowspan=4, sticky="nsew", padx=5, pady=5)

        self.checkpoint_buttons = {}
        self.checkpoint_status_labels = {}

        # Create the checkbuttons and status labels
        for i, (text, var) in enumerate(self.checkpoints.items(), start=1):
            # Create button
            button = ttk.Checkbutton(self.checkpoints_frame, text=text, variable=var, state="disabled")
            button.grid(row=i, column=0, sticky="w", padx=5, pady=5)
            self.checkpoint_buttons[text] = button  # Store reference

            # Create status label
            status_label = ttk.Label(self.checkpoints_frame, text="Unchecked")
            status_label.grid(row=i, column=1, sticky="w", padx=5, pady=5)
            self.checkpoint_status_labels[text] = status_label  # Store reference

        # Fraud Count Label
        self.fraud_label = ttk.Label(video_frame, text=f"Fraud Count: {self.fraud_count_var.get()}")
        self.fraud_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)

        # Video label
        self.video_label = ttk.Label(video_frame)
        self.video_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=2, pady=2)
        self.update_video()

        # Countdown Timer Label
        self.countdown_label = ttk.Label(video_frame, text=f"CountDown: {self.countdown_var.get()}")
        self.countdown_label.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        # Add an instruction label at the top
        ttk.Label(self.checkpoints_frame, text="Please follow the instructions below:").grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=5)

        # Add a label and the Start Reference button at the bottom of checkpoints
        ttk.Label(self.checkpoints_frame, text="Complete the checkpoints to proceed:").grid(row=len(self.checkpoints) + 1, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        self.ref_button = ttk.Button(self.checkpoints_frame, text="Start Reference", command=self.ref_submit)
        self.ref_button.grid(row=len(self.checkpoints) + 2, column=0, columnspan=2, padx=5, pady=5)

        ttk.Label(self.checkpoints_frame, text="If fraud count reaches 10 or timer hits 0, vote will be cancelled").grid(row=len(self.checkpoints) + 3, column=0, columnspan=2, sticky="w", padx=5, pady=5)

        # Voting Instructions frame (below video and checkpoints)
        voting_frame = ttk.LabelFrame(self.form_frame4, text="Voting Panel", padding=(10, 10))
        voting_frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        voting_frame.grid_columnconfigure((0, 1), weight=1)

        # Candidate selection
        candidates = self.db.fetch_candidate()  # Assuming self.db has a method to fetch candidates
        self.radio_buttons = {}

        # Create radio buttons with candidate information in a 2-column grid
        for i, (candidate_id, candidate_info) in enumerate(candidates.items()):
            row, col = divmod(i, 2)
            candidate_frame = ttk.Frame(voting_frame, padding=5)
            candidate_frame.grid(row=row + 1, column=col, sticky="nsew", padx=5, pady=5)
            candidate_frame.grid_columnconfigure(0, weight=1)

            # Load and resize image
            image_path = self.db.download_party_image(f"candidate/{candidate_id}.jpg")
            try:
                response = requests.get(image_path, timeout=10)
                image_data = BytesIO(response.content)
                image = Image.open(image_data)
                image = image.resize((50, 50), Image.LANCZOS)  # Resize if necessary
                photo = ImageTk.PhotoImage(image)
            except Exception as e:
                print(f"Error loading image for candidate {candidate_id}: {e}")
                photo = ImageTk.PhotoImage(Image.new("RGB", (50, 50)))

            image_label = ttk.Label(candidate_frame, image=photo)
            image_label.image = photo  # Keep a reference to avoid garbage collection
            image_label.grid(row=0, column=0, rowspan=3)
 
            # Candidate details
            ttk.Label(candidate_frame, text=candidate_id, font=("Arial", 12)).grid(row=0, column=1, sticky="w", padx=5)
            ttk.Label(candidate_frame, text=candidate_info["name"], font=("Arial", 12)).grid(row=1, column=1, sticky="w", padx=5)
            ttk.Label(candidate_frame, text=candidate_info["party"], font=("Arial", 12)).grid(row=2, column=1, sticky="w", padx=5)

            # Radio button for each candidate
            radio_button = ttk.Radiobutton(
                candidate_frame, text="", variable=self.selected_candidate,
                value=candidate_id, command=lambda cid=candidate_id: self.select_candidate(cid)
            )
            radio_button.grid(row=0, column=2, rowspan=3, sticky="e", padx=10)
            self.radio_buttons[candidate_id] = radio_button

        # Vote Submit Button
        self.vote_submit_button = ttk.Button(voting_frame, text="Submit Vote", command=self.submit_vote, state="disabled")
        self.vote_submit_button.grid(row=len(candidates) // 2 + 1, column=0, pady=10, sticky="e")

        # Back to Home button, initially disabled
        self.back_to_home_button = ttk.Button(voting_frame, text="Back to Home", command=self.back_to_home, state="disabled")
        self.back_to_home_button.grid(row=len(candidates) // 2 + 1, column=1, pady=10, sticky="w")

    def select_candidate(self, candidate_id):
        self.selected_candidate.set(candidate_id)

    def are_all_checkpoints_checked(self):
        # Return True if all checkpoint variables are set to True, otherwise False
        return all(var.get() for var in self.checkpoints.values())


    def update_video(self):
        if self.is_end == False:
            frame, fraud_count, checkpoints = self.facial_verify.get_frame(self.ref_var)  # Assuming a method for frame retrieval

            if frame is not None:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img_tk = ImageTk.PhotoImage(img)
                self.video_label.config(image=img_tk)
                self.video_label.image = img_tk  # Keep a reference to avoid garbage collection

            # Update checkpoints status based on the values from the checkpoints dictionary
            for key, value in checkpoints.items():
                if key in self.checkpoints:
                    self.checkpoints[key].set(value)  # Set the Checkbutton variable to the new value
    
                    # Update the corresponding button text and status label
                    if key in self.checkpoint_buttons:  # Check if the button exists
                        button = self.checkpoint_buttons[key]
                        button.config(text="Checked" if value else "Unchecked", bootstyle="success" if value else "")
    
                    # Update the corresponding status label text
                    if key in self.checkpoint_status_labels:  # Assuming you have a dictionary for status labels
                        status_label = self.checkpoint_status_labels[key]
                        status_label.config(text="Checked" if value else "Unchecked", bootstyle="success" if value else "")

            # Check if all checkpoints are completed
            if self.are_all_checkpoints_checked():
                self.fraud_count_var = fraud_count
                if self.fraud_count_var < 50:
                    # Enable the timer, fraud counter, and voting buttons here
                    self.fraud_label.config(text=f"Fraud Count: {self.fraud_count_var}")
                    if self.start_timer == False:
                        self.timer()
                        self.start_timer = True
                    self.vote_submit_button.config(state="normal")  # Enable the vote submit button
                    self.ref_button.config(state="disabled")  # Disable the reference button after use
                else:
                    self.vote_submit_button.config(state="disabled")
                    self.ref_button.config(state="disabled")
                    self.on_end()

            self.video_label.after(10, self.update_video)  # Update every 10 ms (about 100 FPS)
        else:
            self.video_label.destroy()

    def timer(self, seconds=30):
        # Update the countdown variable and label
        self.countdown_var = seconds
        self.countdown_label.config(text=f"CountDown: {self.countdown_var}s")

        # If there is still time left, update after 1 second
        if seconds > 0:
            self.countdown_label.after(1000, self.timer, seconds - 1)  # Use countdown_label's after method
        else:
            # Countdown finished, take additional action here
            self.countdown_label.config(text="CountDown: Time's up!")
            self.vote_submit_button.config(state="disabled")
            self.ref_button.config(state="disabled")
            self.on_end()


    def on_end(self):
        try:
            candidate_id = "c004"  # Get the selected candidate ID
            aadhaar_number = self.decrypted_data_dict['aadhar_id']
            vote = self.vote.vote(candidate_id, aadhaar_number)  # Assuming a voting method in your app
            if vote:
                messagebox.showinfo("Voted", "You are restricted to vote due to frauding or times up. Your vote is going to 'No Party Preference'.")
                self.vote_submit_button.config(state=DISABLED)
                self.back_to_home_button.config(state="normal")
                self.video_label.destroy()
                self.is_end = True
            else:
                messagebox.showerror("Error", "You already voted")
                self.vote_submit_button.config(state=DISABLED)
                self.back_to_home_button.config(state="normal")
                self.video_label.destroy()
                self.is_end = True
        except Exception as e:
            print("Error:", e)

    def ref_submit(self):
        self.ref_var = True
        self.ref_button.config(state=DISABLED)
        # Start the video capture logic here if needed

    def submit_vote(self):
        try:
            candidate_id = self.selected_candidate.get()  # Get the selected candidate ID
            aadhaar_number = self.decrypted_data_dict['aadhar_id']
            vote = self.vote.vote(candidate_id, aadhaar_number)  # Assuming a voting method in your app
            if vote:
                messagebox.showinfo("Voted", "You have successfully voted.")
                self.back_to_home_button.config(state="normal")
                self.vote_submit_button.config(state="disabled")
                self.ref_button.config(state="disabled")
                self.video_label.destroy()
            else:
                messagebox.showerror("Error", "You already voted")
                self.vote_submit_button.config(state="disabled")
                self.ref_button.config(state="disabled")
                self.back_to_home_button.config(state="normal")
                self.video_label.destroy()
        except Exception as e:
            print("Error:", e)
    

    def submit_tab1(self):
        self.create_tab2()
        self.notebook.tab(0, state="disabled")
        # Move to the next tab
        self.notebook.tab(1, state="normal")
        self.notebook.select(1)

    def submit_tab2(self):
        if self.checkbox_var.get():
            self.create_tab3()
            self.notebook.tab(1, state="disabled")
            # Move to the next tab
            self.notebook.tab(2, state="normal")
            self.notebook.select(2)
        else:
            messagebox.showwarning("Warn", "Please check the box before proceed.")

    def submit_tab3(self):
        self.create_tab4()
        self.notebook.tab(2, state="disabled")
        # Move to the next tab
        self.notebook.tab(3, state="normal")
        self.notebook.select(3)

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

    def back_to_home(self):
        self.app.show_landing_page()
    
    def show(self):
        self.parent_frame.pack(fill="both", expand=True, anchor=CENTER) 

    def hide(self):
        self.parent_frame.pack_forget()