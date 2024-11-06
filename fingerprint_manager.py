import ctypes
from ctypes import wintypes
import binascii
import sys

def is_admin():
    """Check if the script is running with admin privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Constants
SECURITY_MAX_SID_SIZE = 68
WINBIO_TYPE_FINGERPRINT = 0x00000008
WINBIO_POOL_SYSTEM = 0x00000001
WINBIO_FLAG_DEFAULT = 0x00000000
WINBIO_E_NO_MATCH = 0x80098005

# Load the WinBio DLL
winbio = ctypes.WinDLL(r"C:\Windows\System32\winbio.dll")

# Define GUID structure
class GUID(ctypes.Structure):
    _fields_ = [("Data1", wintypes.DWORD),
                ("Data2", wintypes.WORD),
                ("Data3", wintypes.WORD),
                ("Data4", wintypes.BYTE * 8)]

# Define Account SID structure
class AccountSid(ctypes.Structure):
    _fields_ = [("Size", wintypes.ULONG),
                ("Data", ctypes.c_ubyte * SECURITY_MAX_SID_SIZE)]

# Define Value structure (part of WINBIO_IDENTITY)
class Value(ctypes.Union):
    _fields_ = [("NULL", wintypes.ULONG),
                ("Wildcard", wintypes.ULONG),
                ("TemplateGuid", GUID),
                ("AccountSid", AccountSid)]

# Define WINBIO_IDENTITY structure
class WINBIO_IDENTITY(ctypes.Structure):
    _fields_ = [("Type", ctypes.c_uint32),
                ("Value", Value)]

# Define FingerPrint Manager class
class FingerprintManager:
    def __init__(self):
        self.session_handle = ctypes.c_uint32()
        self.unit_id = ctypes.c_uint32()
        self.subfactor = ctypes.c_ubyte(0xf5)
        self.identity = WINBIO_IDENTITY()
        self.is_open = False
        self._fingerprint_database = {}

    @property
    def fingerprint_database(self):
        """Provides access to the fingerprint database."""
        return self._fingerprint_database

    def open_session(self):
        """Open a fingerprint session."""
        if self.is_open:
            return
        result = winbio.WinBioOpenSession(WINBIO_TYPE_FINGERPRINT,
                                           WINBIO_POOL_SYSTEM,
                                           WINBIO_FLAG_DEFAULT,
                                           None, 0, None,
                                           ctypes.byref(self.session_handle))
        if result != 0:
            raise Exception(f"Failed to open session: {hex(result)}")
        self.is_open = True

    def close_session(self):
        """Close the fingerprint session."""
        if self.is_open:
            winbio.WinBioCloseSession(self.session_handle)
            self.is_open = False

    def capture_fingerprint(self):
        """Capture a fingerprint and return its hexadecimal representation."""
        reject_detail = ctypes.c_uint32()
        result = winbio.WinBioIdentify(self.session_handle,
                                       ctypes.byref(self.unit_id),
                                       ctypes.byref(self.identity),
                                       ctypes.byref(self.subfactor),
                                       ctypes.byref(reject_detail))
        if result == WINBIO_E_NO_MATCH:
            print("No match found.")
            return None
        elif result != 0:
            raise Exception(f"Identify Error: {hex(result)}")

        # Convert the captured fingerprint to a string format (hexadecimal)
        fingerprint_bytes = bytearray(self.identity.Value.AccountSid.Data[:self.identity.Value.AccountSid.Size])
        fingerprint_hex = binascii.hexlify(fingerprint_bytes).decode('utf-8')

        return fingerprint_hex

    def save_fingerprint(self, name):
        """Capture and save a fingerprint for a given name."""
        print(f"Capturing fingerprint for {name}. Please touch the sensor...")
        captured_fingerprint = self.capture_fingerprint()
        if captured_fingerprint:
            self.fingerprint_database[name] = captured_fingerprint
            print(f"Fingerprint for {name} saved successfully! {captured_fingerprint}")
            return True
        else:
            print("Fingerprint capture failed.")
            return False

    def validate_fingerprint(self, pre_stored_fingerprint):
            verify_fingerprint = self.capture_fingerprint()
            if verify_fingerprint is not None and pre_stored_fingerprint == verify_fingerprint:
                return True
            else:
                return False
       

# If this script is run as a standalone program
if __name__ == "__main__":
    if not is_admin():
        # Re-run the program with admin privileges
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

    # Initialize FingerprintManager and open session
    # fp_manager = FingerprintManager()
    # fp_manager.open_session()
    # fp_manager.save_fingerprint("User1")
    # fp_manager.validate_fingerprint()
    # fp_manager.update_fingerprint("User1")

    print("Running with Administrator privileges!")
