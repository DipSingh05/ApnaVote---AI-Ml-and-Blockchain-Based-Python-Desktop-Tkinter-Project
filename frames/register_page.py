import cv2
from tkinter import *
from tkinter import filedialog, Toplevel, messagebox
from datetime import datetime, timedelta
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import numpy as np
import json
import re
import os
import base64
from fingerprint_manager import FingerprintManager
from firebase_manager import FirebaseDB
from secure import EncryptHash

class RegisterPage:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app

        # Load states and districts from JSON
        with open('./assets/api/states-and-districts.json', 'r') as f:
            self.data = json.load(f)

        self.states = self.data['states']
        
        # Create a frame to hold the form elements (labels and entries)
        self.parent_frame = ttk.Frame(self.parent, padding=(10,10))

        # Create a canvas to display background image
        self.canvas = Canvas(self.parent_frame)
        self.canvas.place(relheight=1, relwidth=1)

        # Load the image
        self.bg_image = Image.open("./assets/img/background_templete.png")

        # Load init variables
        self.face_image = None
        self.capture_print = False
        self.file_path = None
        self.timestamp = None

        # Bind the resize event to the function on the parent
        self.parent_frame.bind("<Configure>", self.resize_image)

        # Header label for the form
        self.header_label = ttk.Label(self.parent_frame, text="Register Yourself Here!", font=("Arial", 20), width=50,
                                      background='green', foreground="white", padding=10, anchor='center')
        self.header_label.place(relx=0.5, rely=0.08, anchor=CENTER)

        # Create warn Label"
        self.warn_label = ttk.Label(self.parent_frame, text="Check all data correctly before submit. after submition tabs will be close and not accessable again.", font=("Arial", 12), foreground="blue")
        self.warn_label.place(relx=0.5, rely=0.15, anchor=CENTER)

        self.note_label = ttk.Label(self.parent_frame, text="Note:- It's a dummy database, replicating indian citizen criteria's. so, if you are new! then register yourself first..",font=("Arial", 10))
        self.note_label.place(relx=0.5, rely=0.97, anchor=CENTER)

        # Create custom styles for buttons
        self.style = ttk.Style()
        self.style.configure("Submit.TButton",
                             font=("Arial", 12),
                             padding=6,
                             background="green",
                             foreground="white")

        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.parent_frame, padding=(10,10))
        self.notebook.place(relx=0.5, rely=0.56, anchor=CENTER)

        # Create each tab frame
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)
        self.tab4 = ttk.Frame(self.notebook)

        # Add tabs to the notebook
        self.notebook.add(self.tab1, text="Basic Info")
        self.notebook.add(self.tab2, text="Face Capture", state="disabled")
        self.notebook.add(self.tab3, text="Fingerprint", state="disabled")
        self.notebook.add(self.tab4, text="Submit and Upload", state="disabled")

        # --- TAB 1: Basic Info Form ---
        self.create_tab1()
        
        #Initilized fingureprint manager
        self.fp_manager = FingerprintManager()
        self.fp_manager.open_session()

        #Initilized firebase db
        self.db = FirebaseDB()

        #Initilized security
        self.eh = EncryptHash()

    def create_tab1(self):
        # Frame for form elements
        self.form_frame1 = ttk.Frame(self.tab1)
        self.form_frame1.pack(padx=20, pady=20)

        # Create label and entry for "Adhar ID"
        self.adhar_label = ttk.Label(self.form_frame1, text="Adhar ID:", font=("Arial", 14))
        self.adhar_entry = ttk.Entry(self.form_frame1, font=("Arial", 14))
        self.adhar_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.adhar_entry.grid(row=0, column=1, padx=10, pady=10, sticky=W)

        # Create label and entry for "Voter ID"
        self.voter_label = ttk.Label(self.form_frame1, text="Voter ID:", font=("Arial", 14))
        self.voter_entry = ttk.Entry(self.form_frame1, font=("Arial", 14))
        self.voter_label.grid(row=0, column=2, padx=10, pady=10, sticky=E)
        self.voter_entry.grid(row=0, column=3, padx=10, pady=10, sticky=E)

        # Create label and entry for "First Name"
        self.firstname_label = ttk.Label(self.form_frame1, text="First Name:", font=("Arial", 14))
        self.firstname_entry = ttk.Entry(self.form_frame1, font=("Arial", 14))
        self.firstname_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        self.firstname_entry.grid(row=1, column=1, padx=10, pady=10, sticky=W)

        # Create label and entry for "Last Name"
        self.lastname_label = ttk.Label(self.form_frame1, text="Last Name:", font=("Arial", 14))
        self.lastname_entry = ttk.Entry(self.form_frame1, font=("Arial", 14))
        self.lastname_label.grid(row=1, column=2, padx=10, pady=10, sticky=E)
        self.lastname_entry.grid(row=1, column=3, padx=10, pady=10, sticky=E)

         # Get the current year and month
        min_month = datetime.now().month - 1  # Minimum year
        min_year = datetime.now().year - 18  # Maximum year for date of birth

         # Create label and DateEntry for "Date of Birth"
        self.dob_label = ttk.Label(self.form_frame1, text="Date of Birth:", font=("Arial", 14))
        self.dob_entry = ttk.DateEntry(
            self.form_frame1,
            bootstyle = "dark",
            startdate = datetime(min_year,min_month,1),
            dateformat=r"%d-%m-%y"
        )
        self.dob_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)
        self.dob_entry.grid(row=2, column=1, padx=10, pady=10, sticky=W)

        # Create label and entry for "Address"
        self.address_label = ttk.Label(self.form_frame1, text="Address:", font=("Arial", 14))
        self.address_entry = ttk.Entry(self.form_frame1, font=("Arial", 14))
        self.address_label.grid(row=2, column=2, padx=10, pady=10, sticky=E)
        self.address_entry.grid(row=2, column=3, padx=10, pady=10, sticky=E)

        # Create label and dropdown for "Gender"
        self.gender_label = ttk.Label(self.form_frame1, text="Gender:", font=("Arial", 14))
        self.gender_var = StringVar()
        self.gender_dropdown = ttk.Combobox(self.form_frame1, textvariable=self.gender_var, values=["Male", "Female", "Other"], font=("Arial", 14))
        self.gender_label.grid(row=3, column=0, padx=10, pady=10, sticky=W)
        self.gender_dropdown.grid(row=3, column=1, padx=10, pady=10, sticky=W)

        # Create label and entry for "Phone"
        self.phone_label = ttk.Label(self.form_frame1, text="Phone:", font=("Arial", 14))
        self.phone_entry = ttk.Entry(self.form_frame1, font=("Arial", 14))
        self.phone_label.grid(row=3, column=2, padx=10, pady=10, sticky=E)
        self.phone_entry.grid(row=3, column=3, padx=10, pady=10, sticky=E)

        # Create label and dropdown for "State"
        self.state_label = ttk.Label(self.form_frame1, text="State:", font=("Arial", 14))
        self.state_var = StringVar()
        self.state_dropdown = ttk.Combobox(self.form_frame1, textvariable=self.state_var, values=[state['state'] for state in self.states], font=("Arial", 14), state='readonly')
        self.state_label.grid(row=4, column=0, padx=10, pady=10, sticky=W)
        self.state_dropdown.grid(row=4, column=1, padx=10, pady=10, sticky=W)
        self.state_dropdown.bind("<<ComboboxSelected>>", self.populate_districts)

        # Create label and dropdown for "District"
        self.district_label = ttk.Label(self.form_frame1, text="District:", font=("Arial", 14))
        self.district_var = StringVar()
        self.district_dropdown = ttk.Combobox(self.form_frame1, textvariable=self.district_var, font=("Arial", 14), state='readonly')
        self.district_label.grid(row=4, column=2, padx=10, pady=10, sticky=E)
        self.district_dropdown.grid(row=4, column=3, padx=10, pady=10, sticky=E)

        # Create label and entry for "PIN"
        self.pin_label = ttk.Label(self.form_frame1, text="PIN:", font=("Arial", 14))
        self.pin_entry = ttk.Entry(self.form_frame1, font=("Arial", 14))
        self.pin_label.grid(row=5, column=0, padx=10, pady=10, sticky=W)
        self.pin_entry.grid(row=5, column=1, padx=10, pady=10, sticky=W)

        # Create label and entry for "Is Linked"
        self.islinked_label = ttk.Label(self.form_frame1, text="Is Linked:", font=("Arial", 14))
        self.islinked_var = StringVar()
        self.islinked_dropdown = ttk.Combobox(self.form_frame1, textvariable=self.islinked_var, values=["Yes", "No"], font=("Arial", 14))
        self.islinked_label.grid(row=5, column=2, padx=10, pady=10, sticky=E)
        self.islinked_dropdown.grid(row=5, column=3, padx=10, pady=10, sticky=E)

        # Create label and entry for "Email"
        self.email_label = ttk.Label(self.form_frame1, text="Email:", font=("Arial", 14))
        self.email_entry = ttk.Entry(self.form_frame1, font=("Arial", 14))
        self.email_label.grid(row=6, column=0, padx=10, pady=10, sticky=W)
        self.email_entry.grid(row=6, column=1, padx=10, pady=10, sticky=W)

        # Create label and entry for "Citizen"
        self.Citizen_label = ttk.Label(self.form_frame1, text="Citizen:", font=("Arial", 14))
        self.Citizen_var = StringVar()
        self.Citizen_dropdown = ttk.Combobox(self.form_frame1, textvariable=self.Citizen_var, values=["India"], font=("Arial", 14))
        self.Citizen_label.grid(row=6, column=2, padx=10, pady=10, sticky=E)
        self.Citizen_dropdown.grid(row=6, column=3, padx=10, pady=10, sticky=E)

        # Center the submit button
        self.submit_tab1_button = ttk.Button(self.form_frame1, text="Submit", style="Submit.TButton", padding=(10,10), command=self.submit_tab1)
        self.submit_tab1_button.grid(row=7, column=0, columnspan=4, pady=20)

    def populate_districts(self, event):
        """Populate the district dropdown based on the selected state."""
        selected_state = self.state_var.get()
        districts = next((state['districts'] for state in self.states if state['state'] == selected_state), [])
        self.district_dropdown['values'] = districts
        self.district_dropdown.set('')


    def upload_image(self):
        # Open file dialog to select an image
        self.file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if self.file_path:
            # Check and resize image
            if not self.check_image_size(self.file_path):
                return  # If resizing was needed and not valid, exit

            # Load the resized image to fit within the label
            image = Image.open(self.file_path)
            image = image.resize((250, 250), Image.LANCZOS)
            self.face_image = ImageTk.PhotoImage(image)

            # Display the image in the label
            self.image_label.config(image=self.face_image)
            self.image_label.image = self.face_image

    def check_image_size(self, file_path):
        # Check the size of the image
        size_kb = os.path.getsize(file_path) / 1024  # Size in KB
        if size_kb > 100:  # Image exceeds 20 KB
            if os.path.getsize(file_path) / 1024 > 100:
                # Resize and compress the image
                self.resize_and_compress_image(file_path)
                messagebox.showerror("Error", "Image could not be resized to under 100 KB.")
                self.capture_window.destroy()
                return False  # Image still too large
        return True  # Image size is valid

    def resize_and_compress_image(self, file_path):
        # Resize and compress the image
        with Image.open(file_path) as img:
            img = img.resize((250, 250), Image.LANCZOS)
            img.save(file_path, optimize=True, quality=86)  # Adjust quality as needed
            img.save(file_path)

    def capture_image(self):
        self.capture_window = Toplevel()
        self.capture_window.title("Align Face and Capture")
        self.capture_window.geometry("720x600")

        self.warning_label = ttk.Label(self.capture_window, text="Capture in the bright area", font=("Arial", 12), foreground="blue")
        self.warning_label.pack(pady=5)

        self.video_label = Label(self.capture_window, height=480, width=720)
        self.video_label.pack(padx=10, pady=10, anchor="center")

        self.capture_button = ttk.Button(self.capture_window, text="Capture", style="Submit.TButton", command=self.capture_frame, state="disabled")
        self.capture_button.pack(pady=10)

        self.capture_window.protocol("WM_DELETE_WINDOW", self.close_capture_window)

        self.cap = cv2.VideoCapture(0)
        self.show_video_feed()

    def close_capture_window(self):
        if self.cap.isOpened():
            self.cap.release()
        self.capture_window.destroy()

    def show_video_feed(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.resize(frame, (720, 480))
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            brightness_level = np.mean(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))

            if brightness_level < 80:
                self.warning_label.config(text="Brightness too low. Please adjust lighting.", foreground="red")
                self.capture_button.config(state="disabled")
            else:
                self.warning_label.config(text="Capture in the bright area", foreground="blue")
                self.capture_button.config(state="normal")

            image = Image.fromarray(frame_rgb)
            self.face_image = ImageTk.PhotoImage(image)

            self.video_label.config(image=self.face_image)
            self.video_label.image = self.face_image

        self.capture_window.after(6, self.show_video_feed)

    def capture_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame_rgb)
            image = image.resize((250, 250), Image.LANCZOS)

            # Format the datetime to remove invalid characters
            self.timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Use underscore instead of colon

            # Save the captured image to a temporary file
            temp_image_path = f"./assets/face/{self.timestamp}.png"
            image.save(temp_image_path)
            self.file_path = temp_image_path

            # Check and compress the image
            if not self.check_image_size(temp_image_path):
                return  # Exit if image is still too large

            # Convert to a format Tkinter can use
            self.face_image = ImageTk.PhotoImage(image)

            # Display captured image in the Face Capture tab
            self.image_label.config(image=self.face_image)
            self.image_label.image = self.face_image
            
            # Close the capture window
            self.cap.release()
            self.capture_window.destroy()

    def create_tab2(self):
        self.face_label = ttk.Label(self.tab2, text="Capture Face Image Here", font=("Arial", 16))
        self.face_label.pack(pady=20)

        button_frame = ttk.Frame(self.tab2)
        button_frame.pack(pady=10)

        self.upload_button = ttk.Button(button_frame, text="Upload from Desktop", style="Submit.TButton", padding=(10, 10), command=self.upload_image)
        self.upload_button.grid(row=0, column=0, padx=10)

        self.capture_button = ttk.Button(button_frame, text="Capture from Camera", style="Submit.TButton", padding=(10, 10), command=self.capture_image)
        self.capture_button.grid(row=0, column=1, padx=10)

        self.image_label = ttk.Label(self.tab2)
        self.image_label.pack(pady=20)

        self.submit_tab2_button = ttk.Button(self.tab2, text="Submit", style="Submit.TButton", padding=(10, 10), command=self.submit_tab2)
        self.submit_tab2_button.pack(pady=20)

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
        # Check if fingerprint_database is empty or None
        if not self.fp_manager.fingerprint_database:
            self.status_label.config(text="Place one finger in scanner", foreground="blue")
            self.status_label.update_idletasks()
            self.capture_print = self.fp_manager.save_fingerprint(self.aadhar_entry.get() or "User1")
            if self.capture_print:
                messagebox.showinfo("Success", "Fingerprint registered successfully.")
                self.status_label.destroy()
                self.fp_manager.close_session()
            else:
                messagebox.showerror("Error", "Error during fingerprint registration.")
                self.status_label.config(text="Click on the scan button", foreground="black")
                self.status_label.update_idletasks()
                self.fp_manager.close_session()
        else:
            messagebox.showwarning("Warning", "Already fingerprint registered.")
            self.fp_manager.close_session()
       
        # # Enable or disable the submit button based on capture status
        self.scan_button.config(state="disabled" if self.capture_print else "normal")

    def validate_entries(self):
        # Retrieve values
        aadhar_id = self.aadhar_entry.get()
        voter_id = self.voter_entry.get()
        first_name = self.firstname_entry.get()
        last_name = self.lastname_entry.get()
        dob = self.dob_entry.entry.get()
        address = self.address_entry.get()
        gender = self.gender_var.get()
        state = self.state_var.get()
        district = self.district_var.get()
        pin = self.pin_entry.get()
        is_linked = self.islinked_var.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()

         # Print all retrieved values
        print(f"Aadhaar ID: {aadhar_id}")
        print(f"Voter ID: {voter_id}")
        print(f"First Name: {first_name}")
        print(f"Last Name: {last_name}")
        print(f"Date of Birth: {dob}")
        print(f"Address: {address}")
        print(f"Gender: {gender}")
        print(f"State: {state}")
        print(f"District: {district}")
        print(f"PIN: {pin}")
        print(f"Is Linked: {is_linked}")
        print(f"Phone Number: {phone}")
        print(f"Email: {email}")

        #Calculate the required date that is exactly 18 years ago from today
        required_date = datetime.now() - timedelta(days=18 * 365)  # Approximation of 18 years
    
        # Error message setup
        error_message = ""
        email_pattern = r"^[a-zA-Z0-9_.]+@gmail\.com$"

        # 1. Check for empty fields
        if all([aadhar_id, voter_id, first_name, last_name, dob, address, gender, state, district, pin, phone, email]):
    
            # 2. Validate Date of Birth
            try:
                dob_date = datetime.strptime(dob, "%d-%m-%y")
                if dob_date < required_date:
            
                    # 3. Aadhaar validation: 12 numeric characters
                    if aadhar_id.isdigit() and len(aadhar_id) == 12:
                
                        # 4. Voter ID validation: 10 alphanumeric characters
                        if voter_id.isalnum() and len(voter_id) == 10:
                    
                            # 5. Phone number validation: 10 digits
                            if phone.isdigit() and len(phone) == 10:
                        
                                # 6. Email validation: valid Gmail format
                                if re.match(email_pattern, email):
                            
                                    # 7. PIN validation: 6 numeric characters
                                    if pin.isdigit() and len(pin) == 6:
                                        return True
                                    else:
                                        error_message = "PIN must be exactly 6 numeric characters."
                                else:
                                    error_message = "Email must be a valid Gmail address (e.g., user@gmail.com) with only letters, numbers, '_', or '.'."
                            else:
                                error_message = "Phone number must be exactly 10 digits."
                        else:
                            error_message = "Voter ID must be exactly 10 alphanumeric characters."
                    else:
                        error_message = "Aadhaar ID must be exactly 12 numeric characters."
                else:
                    error_message = "Age must be at least 19 years."
            except ValueError:
                error_message = "Invalid date format for DOB. Use DD-MM-YYYY."
        else:
            error_message = "All fields must be filled."

        # Display error message if validation fails
        if error_message:
            messagebox.showerror("Error", f"{error_message}")
            return False

    def create_tab4(self):
        # Title Label for Summary Page
        summary_label = ttk.Label(self.tab4, text="Summary of Registration", font=("Arial", 16, "bold"))
        summary_label.pack(padx=10, pady=10, anchor=CENTER)

        # Create the main frame for the summary in Tab 4
        self.form_frame2 = ttk.Frame(self.tab4)
        self.form_frame2.pack(padx=10, pady=10)
    
        # Name Fields
        name_frame = ttk.LabelFrame(self.form_frame2, text="Name Information", padding=(10,10), bootstyle="success")
        name_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        ttk.Label(name_frame, text=f"First Name: {self.firstname_entry.get()}").grid(row=0, column=0, sticky="w", padx=2, pady=2)
        ttk.Label(name_frame, text=f"Last Name: {self.lastname_entry.get()}").grid(row=1, column=0, sticky="w", padx=2, pady=2)

        # Display Photo
        photo_frame = ttk.LabelFrame(self.form_frame2, text="Photo", padding=(10,10), bootstyle="success")
        photo_frame.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        cover_image = Image.open(self.file_path)  # Open the image file
        photo = ImageTk.PhotoImage(cover_image.resize((50, 50), Image.LANCZOS))
        photo_label = ttk.Label(photo_frame, image=photo, text=f"{self.timestamp}.png", compound="left")
        photo_label.grid(row=0, column=0, padx=2, pady=2)
        self.photo_display = photo  # Keep a reference to avoid garbage collection
    
        # Aadhaar and Voter IDs
        id_frame = ttk.LabelFrame(self.form_frame2, text="ID Information", padding=(10,10), bootstyle="success")
        id_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        ttk.Label(id_frame, text=f"Aadhaar ID: {self.aadhar_entry.get()}").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        ttk.Label(id_frame, text=f"Voter ID: {self.voter_entry.get()}").grid(row=1, column=0, sticky="w", padx=5, pady=2)
    
        # Personal Information (DOB, Gender)
        personal_frame = ttk.LabelFrame(self.form_frame2, text="Personal Information", padding=(10,10), bootstyle="success")
        personal_frame.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        ttk.Label(personal_frame, text=f"Date of Birth: {self.dob_entry.entry.get()}").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        ttk.Label(personal_frame, text=f"Gender: {self.gender_var.get()}").grid(row=1, column=0, sticky="w", padx=5, pady=2)
    
        # Address Information (Address, State, District, PIN)
        address_frame = ttk.LabelFrame(self.form_frame2, text="Address Information", padding=(10,10), bootstyle="success")
        address_frame.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        ttk.Label(address_frame, text=f"Address: {self.address_entry.get()}").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        ttk.Label(address_frame, text=f"State: {self.state_var.get()}").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        ttk.Label(address_frame, text=f"District: {self.district_var.get()}").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        ttk.Label(address_frame, text=f"PIN: {self.pin_entry.get()}").grid(row=3, column=0, sticky="w", padx=5, pady=2)
    
        # Contact Information (Phone, Email)
        contact_frame = ttk.LabelFrame(self.form_frame2, text="Contact Information", padding=(10,10), bootstyle="success")
        contact_frame.grid(row=3, column=1, sticky="ew", padx=5, pady=5)
        ttk.Label(contact_frame, text=f"Phone: +91-{self.phone_entry.get()}").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        ttk.Label(contact_frame, text=f"Email: {self.email_entry.get()}").grid(row=1, column=0, sticky="w", padx=5, pady=2)
    
        # Linked Status
        linked_frame = ttk.LabelFrame(self.form_frame2, text="Linkage Status", padding=(10,10), bootstyle="success")
        linked_frame.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
        ttk.Label(linked_frame, text=f"Linked to Aadhaar: {'Yes' if self.islinked_var.get() else 'No'}").grid(row=0, column=0, sticky="w", padx=5, pady=2)
    
        # Display Fingerprint
        fingerprint_frame = ttk.LabelFrame(self.form_frame2, text="Fingerprint", padding=(10,10), bootstyle="success")
        fingerprint_frame.grid(row=4, column=1, sticky="ew", padx=5, pady=5)
        ttk.Label(fingerprint_frame, text="Fingerprint Captured Successfully").grid(row=0, column=0, padx=5, pady=2)

        
        # Buttons for Upload and Return to Home
        button_frame = ttk.Frame(self.form_frame2)
        button_frame.grid(row=9, column=0, columnspan=2, pady=(20, 10))
    
        self.upload_button = ttk.Button(button_frame, text="Upload", style="Submit.TButton", command=self.submit_tab4)
        self.upload_button.grid(row=0, column=0, padx=10)

        self.home_button = ttk.Button(button_frame, text="Return to Home", style="Submit.TButton", state=DISABLED, command=self.on_back)
        self.home_button.grid(row=0, column=1, padx=10)

        self.bar = ttk.Progressbar(self.tab4, length=100, mode='determinate', value=1, bootstyle="success-striped")
        self.bar.pack(padx=20, pady=10, side="bottom", fill=BOTH, expand=TRUE)

    # Call this function before enabling the next tab
    def submit_tab1(self):
        if self.validate_entries():
            # --- TAB 2: Face Capture Form ---
            self.create_tab2()
            self.notebook.tab(0, state="disabled")
            # Move to the next tab
            self.notebook.tab(1, state="normal")
            self.notebook.select(1)

    def submit_tab2(self):
        if not self.face_image:
             messagebox.showerror("Error", "No image data here.")
        else:
            print("Face capture submitted!")
            if hasattr(self, 'error_label'):
                self.error_label.destroy()
            
            # --- TAB 3: Fingerprint Capture Form ---
            self.create_tab3()

            self.notebook.tab(1, state="disabled")
            # Enable and switch to the Fingerprint tab
            self.notebook.tab(2, state="normal")
            self.notebook.select(2)

    def submit_tab3(self):
        fingerprint = self.capture_print
        if fingerprint == False:
            messagebox.showerror("Error", "No fingerprint data here.")
        else:
             # --- TAB 4: Submittion Form ---
            self.create_tab4()

            self.notebook.tab(2, state="disabled")
            # Enable and switch to the Fingerprint tab
            self.notebook.tab(3, state="normal")
            self.notebook.select(3)

    def submit_tab4(self):
        try:
            uploadtime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            
            data_dict = {
            "aadhar_id": self.aadhar_entry.get(),
            "voter_id": self.voter_entry.get(),
            "first_name": self.firstname_entry.get(),
            "last_name": self.lastname_entry.get(),
            "dob": self.dob_entry.entry.get(),
            "address": self.address_entry.get(),
            "gender": self.gender_var.get(),
            "state": self.state_var.get(),
            "district": self.district_var.get(),
            "pin": self.pin_entry.get(),
            "is_linked": self.islinked_var.get(),
            "phone": self.phone_entry.get(),
            "email": self.email_entry.get(),
            "fingerprint" : self.fp_manager.fingerprint_database[self.aadhar_entry.get()],
            "datetime": uploadtime
            }

            hash_aadhar = self.aadhar_entry.get()

            # Encrypt each value in the dictionary
            # Encrypt and encode the values to make them JSON serializable
            encrypted_data_dict = {
                key: base64.b64encode(self.eh.encrypt_data(value, False)).decode('utf-8') if isinstance(self.eh.encrypt_data(value, False), bytes) else self.eh.encrypt_data(value, False)
                for key, value in data_dict.items()
            }
            # Read the image in binary mode
            with open(self.file_path, "rb") as img_file:
                image_data = img_file.read()

            # Encrypt the image data
            encrypted_data = self.eh.encrypt_data(image_data, isimg=True)  # Assuming encrypt_data method
            bin_file_path = f"./assets/face/bin/{uploadtime}.bin"
            encrypted_storage_path = f"encrypted_images/{uploadtime}.bin"


            # Save encrypted data to a .bin file
            with open(bin_file_path, "wb") as bin_file:
                bin_file.write(encrypted_data)

            # Upload to database
            result_1 = self.db.add_user(hash_aadhar, encrypted_data_dict=encrypted_data_dict)
            if result_1:
                self.bar.config(value=50)
                self.bar.update_idletasks()
                result_2 = self.db.upload_image(bin_file_path, encrypted_storage_path)
                if result_2:
                    self.bar.config(value=100)
                    self.bar.update_idletasks()
                    self.upload_button.config(state=DISABLED)
                    self.home_button.config(state="normal")

        except Exception as e:
            print(f"Failed : {e}")


    def resize_image(self, event):
        new_width = event.width
        new_height = event.height
        resized_image = self.bg_image.resize((new_width, new_height), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(0, 0, image=bg_photo, anchor=NW)
        self.canvas.bg_photo = bg_photo

    def on_back(self):
        self.app.show_landing_page()  # Switch back to landing page

    def show(self):
        self.parent_frame.pack(fill="both", expand=True) 

    def hide(self):
        self.parent_frame.pack_forget()
