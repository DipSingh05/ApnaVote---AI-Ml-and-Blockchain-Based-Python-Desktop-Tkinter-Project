


https://github.com/user-attachments/assets/c81b4913-2c12-49ad-ab97-d63ab8656ad1


# ApnaVote---AI-Ml-and-Blockchain-

Based-Python-Desktop-Tkinter-Project
ApnaVote is a secure Python-based voting app using Tkinter, AI/ML, Firebase, and blockchain. It enables one-time voting with AI facial verification and tamper-proof blockchain storage. Firebase manages voter and candidate data, while smart contracts handle real-time results and candidate updates.

## Demo Images

![apnavote_video - Made with Clipchamp-0](https://github.com/user-attachments/assets/bdda43a8-e72e-4d36-adda-db7c2397a606)
![apnavote_video - Made with Clipchamp-1](https://github.com/user-attachments/assets/cf183e16-b8da-4540-8b72-a57c59952edd)
![apnavote_video - Made with Clipchamp-2](https://github.com/user-attachments/assets/3133ee4c-bb32-439f-8b4b-98414d9360df)
![apnavote_video - Made with Clipchamp-3](https://github.com/user-attachments/assets/193bb9ed-81f0-4ef2-af69-7497a6cf2a2f)
![apnavote_video - Made with Clipchamp-4](https://github.com/user-attachments/assets/cce03044-7ddb-4459-838a-cd6e2bedbbb3)


## Features

1. **Secure Verification**: Utilizes AI facial recognition to verify voters, ensuring only authenticated users can participate. The app includes fraud detection safeguards such as head movement tracking, mouth and face detection, and sound monitoring.
2. **Blockchain-backed Voting**: Votes are stored on the blockchain to maintain data integrity, prevent tampering, and ensure transparency.
3. **Firebase Integration**: Firebase is used to store and retrieve voter and candidate details, enabling quick access and data reliability.
4. **Smart Contracts**: Smart contracts in Web3 manage candidate details, vote storage, and result display, with options to add or remove candidates securely.
5. **One-Time Voting**: Each verified user (via Aadhaar or voter ID) can vote only once, ensuring election integrity.

## Technologies Used

- **Python**: Core programming language for backend logic and functionality.
- **Tkinter**: Provides the GUI for a user-friendly voting experience.
- **AI/ML**: Facial recognition and fraud detection using machine learning models.
- **Firebase**: Cloud database for storing user details, candidate information, and more.
- **Blockchain (Web3)**: Stores votes and manages candidate data, ensuring security and immutability.
- **Twillio**: Handles OTP verification for secure login.

## Note:

Please install python 3.12 ! i checked on another plus version it not worked so.

## How to Run

### 1. Clone the Project

First, clone this repository to your local machine:

```bash
git clone https://github.com/DipSingh05/ApnaVote---AI-Ml-and-Blockchain-Based-Python-Desktop-Tkinter-Project.git
cd ApnaVote
```

### 2. Install Requirements

Install all necessary dependencies by running:

install node.js and cmake

```bash
npm install
pip install -r requirements.txt
```

### 3. Set Up Firebase!
1. Create a Firebase account and set up a new project.
2. SetUp the Realtime Database, set all rules to allow read and write. Manually write The Candidate section. ###"Note. The last c004 will always be same as shown in picture'No party preference'"![Screenshot 2024-11-06 092524](https://github.com/user-attachments/assets/3ecd12af-f265-43bd-852e-3c9e1ab66ade)
![Screenshot 2024-11-06 092459](https://github.com/user-attachments/assets/ddda40bb-f0a2-4d76-bdbd-a565aa963a33)
3. Setup the firebase storage and set all rules allow read and write. Manually create the candidate folder and upload pictures according to same name as given in demo.![Screenshot 2024-11-06 092609](https://github.com/user-attachments/assets/688bc890-4c43-4b85-8714-5c0bf5792722)
![Screenshot 2024-11-06 092556](https://github.com/user-attachments/assets/33fb4fd7-0143-453c-a4da-7034d0a3d871)
![Screenshot 2024-11-06 092716](https://github.com/user-attachments/assets/8fdad0a6-1e54-43cc-85ba-52722ddb5e34)
4.Download the servicekey and save it in assets/json folder as it shown.![Screenshot 2024-11-06 092811](https://github.com/user-attachments/assets/e3794d43-e551-4a41-bbc5-99ab5a679902)
![Screenshot 2024-11-06 091452](https://github.com/user-attachments/assets/6570ba08-abb9-44ef-ad95-056ef25a905f)

5. Copy the Firebase configuration tokens and paste them in `firebase_manager.py` as specified in the file. NOTE WHILE PASTEING BUCKET PLEASE REMOVE(gs://) OTHERWISE IT WILL CREATE PROBLEM![Screenshot 2024-11-06 091349](https://github.com/user-attachments/assets/5cc34562-a272-4178-8b55-575af25d9a6a)
![Screenshot 2024-11-06 091325](https://github.com/user-attachments/assets/d47335d1-2f2d-4bc8-a7c4-191c7df509f6)


### 4. Set Up Twilio for OTP Verification

1. Create a Twilio account.
2. Obtain your Twilio API tokens and paste them in the designated area in `otp_manager.py`.![Screenshot 2024-11-06 093017](https://github.com/user-attachments/assets/a1c6f9be-5930-4ee0-9cc0-7d42176c46b9)


### 5. Run the Application
install cmake, python12, node.js, ganache
Make sure You install 'cmake' and set the visual studio to 'c++ devleopment cmake'- something like that a checkbox will come.. select it with 'python development' while install.
With everything set up, reopen the application, you can now run the app, open 4 command prompt and run the code individually:

```bash
cd votingsystem
truffle init
truffle compile
```
The above code will run one time only if you don't cange the .sol file. without this everything will run all time.

 ```bash
cd votingsystem
ganache
```
Don't close this once it run

 ```bash
cd votingsystem
truffle migrate --reset
```

 ```bash
python apnavote.py
```

## Contributing

Feel free to make changes and improvements to ApnaVote! Contributions are always welcome to help make the application even better.

---

Enjoy a secure and transparent voting experience with ApnaVote!
