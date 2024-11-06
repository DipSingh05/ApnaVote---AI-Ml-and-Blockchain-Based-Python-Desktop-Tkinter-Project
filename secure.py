import bcrypt
from cryptography.fernet import Fernet
import os
import base64

class EncryptHash:
    def __init__(self):
        """Initialize the EncryptHash class with an encryption key."""
        # Define the path to save the key
        self.KEY_FILE_PATH = "./assets/keys/secret.key"
        
        # Load or generate the encryption key
        self.encryption_key = self.load_or_generate_key()
        self.cipher = Fernet(self.encryption_key)

    def load_or_generate_key(self):
        """Load an existing key or generate a new one if not found."""
        # Check if the key file exists
        if os.path.exists(self.KEY_FILE_PATH):
            with open(self.KEY_FILE_PATH, "rb") as key_file:
                key = key_file.read()
        else:
            # Generate a new key and save it to the file
            key = Fernet.generate_key()
            os.makedirs(os.path.dirname(self.KEY_FILE_PATH), exist_ok=True)
            with open(self.KEY_FILE_PATH, "wb") as key_file:
                key_file.write(key)
        return key

    def hash_data(self, data):
        """Generate a bcrypt hash of the input data."""
        salt = bcrypt.gensalt()
        data_hash = bcrypt.hashpw(data.encode(), salt)
        return data_hash

    def check_data(self, data, hashed_data):
        """Check if the provided data matches the hashed data."""
        return bcrypt.checkpw(data.encode(), hashed_data)

    def encrypt_data(self, data, isimg=False):
        """Encrypt the input data. Set `isimg` to True for binary data, or False for strings."""
        if isinstance(data, str) and not isimg:
            # Encrypt as a string
            encrypted_data = self.cipher.encrypt(data.encode())
        elif isinstance(data, bytes) or isimg:
            # Encrypt as binary data
            encrypted_data = self.cipher.encrypt(data)
        else:
            raise ValueError("Data type must be string or bytes.")
        return encrypted_data

    def decrypt_data(self, encrypted_data):
        """Decrypt the encrypted data."""
        # Decode from Base64 if encrypted_data is a string
        if isinstance(encrypted_data, str):
            try:
                encrypted_data_bytes = base64.urlsafe_b64decode(encrypted_data)
            except Exception as e:
                print(f"Error decoding base64: {e}")
                return None
        else:
            encrypted_data_bytes = encrypted_data

        # Decrypt the binary data
        try:
            decrypted_data = self.cipher.decrypt(encrypted_data_bytes)

            # Decode to a string if the decrypted data is ASCII text
            try:
                return decrypted_data.decode()
            except UnicodeDecodeError:
                # Return raw bytes if data is not UTF-8 compatible
                return decrypted_data

        except Exception as e:
            print(f"Error decrypting data: {e}")
            return None

# Example usage
if __name__ == "__main__":
    # encryptor = EncryptHash()
    
    # # The encrypted data you want to decrypt
    # encrypted_value = "Z0FBQUFBQm5JRnJmVHBHcFBrN1R3SkZoaEE2NG5YVkZldlVFcGNHakh3WFZjLUJGNlpqdHFuSy1TSkpNdC1MZEE0cnRLOEJJcTIxbjByc08zeVlybEUzUjRJbUt0dG5URUE9PQ=="

    # # Decrypt the value
    # decrypted_data = encryptor.decrypt_data(encrypted_value)
    # print(decrypted_data)
    pass