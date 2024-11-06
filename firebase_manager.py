import datetime
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import os
import base64
import datetime

from secure import EncryptHash  # Assuming you have a 'secure.py' file with EncryptHash class

class FirebaseDB:
    def __init__(self):
        # Initialize FirebaseDB
        self.service_account_path = r'paste here your firebase service json file' #D:\Apnavote\assets\json\apnavote-52459-firebase-adminsdk-ran0k-aba9bfe0f5.json -- Just for example/ It's mine!!
        self.database_url = 'paste your database url here'
        self.citizen_reference = "/citizen"
        self.candidate_reference = "/candidate"
        self.images_reference = "/encrypted_images"  # Reference to encrypted images
        # Initialize Firebase Storage
        self.bucket_url = 'paste your bucket(firebase storage) url here'

        """Initialize the Firebase app with the given service account and database URL."""

        if not firebase_admin._apps:
            self.cred = credentials.Certificate(self.service_account_path)
            self.app = firebase_admin.initialize_app(self.cred, {
                'databaseURL': self.database_url,
                'storageBucket': self.bucket_url
            })
        else:
            self.app = firebase_admin.get_app()

        self.users_ref = db.reference(self.citizen_reference)
        self.candidate_ref = db.reference(self.candidate_reference)
        self.bucket = storage.bucket()

    def get_secret_document(self, refer):
        """Fetch the secret document from the database."""
        try:
            ref = db.reference(refer)
            return ref.get()
        except Exception as e:
            return None

    def add_user(self, username: str, encrypted_data_dict: dict | str):
        """Add a new user to the 'users' node in the database."""
        try:
            self.users_ref.child(username).set(encrypted_data_dict)
            return True
        except Exception as e:
            return False

    def fetch_user(self, username: str):
        """Fetch user data from the 'users' node in the database."""
        try:
            user_data = self.users_ref.child(username).get()
            if user_data:
                return user_data
            else:
                return None
        except Exception as e:
            return None

    def upload_image(self, file_path: str, storage_path: str):
        """Upload an image to Firebase Cloud Storage."""
        try:
            # Check if the file exists locally
            if not os.path.exists(file_path):
                return False
        
            # Create a new blob and upload the file
            blob = self.bucket.blob(storage_path)
            blob.upload_from_filename(file_path)
            # Check if file exists
            if os.path.exists(file_path):
                os.remove(file_path)
            else:
                return False
            return True
        except FileNotFoundError as fnf_error:
            print(fnf_error)
            return False
        except Exception as e:
            return False

    def download_image(self, storage_path: str, local_path: str):
        """Download an image from Firebase Storage and save it locally."""
        try:
            blob = self.bucket.blob(storage_path)  # Use the dynamic storage_path
            blob.download_to_filename(local_path)
            return True
        except Exception as e:
            return False

    # Party Candidate 

    def add_candidate(self, username: str, encrypted_data_dict: dict | str):
        """Add a new user to the 'users' node in the database."""
        try:
            self.candidate_ref.child(username).set(encrypted_data_dict)
            return True
        except Exception as e:
            return False

    def fetch_candidate(self):
        """Fetch all candidate data from the 'users' node in the database."""
        try:
            # Fetch all data from the 'users' node
            user_data = self.candidate_ref.get()
            if user_data:
                return user_data  # Return the full dataset
            else:
                print("No data found in 'users' node.")
                return None
        except Exception as e:
            print(f"An error occurred while fetching candidate data: {e}")
            return None


    def upload_party_image(self, file_path: str, storage_path: str):
        """Upload an image to Firebase Cloud Storage."""
        try:
            # Check if the file exists locally
            if not os.path.exists(file_path):
                return False
        
            # Create a new blob and upload the file
            blob = self.bucket.blob(storage_path)
            blob.upload_from_filename(file_path)
            # Check if file exists
            if os.path.exists(file_path):
                os.remove(file_path)
            else:
                return False
            return True
        except FileNotFoundError as fnf_error:
            print(fnf_error)
            return False
        except Exception as e:
            return False

    def download_party_image(self, storage_path: str) -> str:
        """Generate a signed URL for an image in Firebase Storage with a 30-second expiration."""
        try:
            # Reference the file in storage using the provided storage_path
            blob = self.bucket.blob(storage_path)
        
            # Generate a signed URL with a 30-second expiration
            image_url = blob.generate_signed_url(expiration=datetime.timedelta(seconds=30))
        
            return image_url
        except Exception as e:
            print(f"Error generating image URL: {e}")
            return False



if __name__ == "__main__":
    # firebase_db = FirebaseDB()
    # print(firebase_db.fetch_user(123456789012))
    # image_url = firebase_db.download_party_image("c001.jpg")
    # print(image_url)  # This will print the signed URL for the image, valid for 30 seconds.
    pass

    
