from web3 import Web3
import json
import sys
import os
from web3.exceptions import ContractLogicError

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
# Now you can import FirebaseDB from firebase_manager.py
from firebase_manager import FirebaseDB
from secure import EncryptHash

class VotingSystem:
    def __init__(self):

        self.db = FirebaseDB()

        # Connect to Ganache
        self.w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
        
        # Check if connected
        if not self.w3.is_connected():
            raise ConnectionError("Failed to connect to Ganache")
        
        print("Connected to Ganache")
        
        self.w3.eth.defaultAccount = self.w3.eth.accounts[0]  # Use the first account
        print(f"Default account set to: {self.w3.eth.defaultAccount}")

        latest_block = self.w3.eth.block_number
        print(f"Latest Block Number: {latest_block}")

        balance = self.w3.eth.get_balance(self.w3.eth.defaultAccount)
        balance_in_ether = self.w3.from_wei(balance, 'ether')
        print(f"Balance of default account: {balance_in_ether} ETH")

        # Load contract ABI and address
        with open(r"D:\Apnavote\votingsystem\build\contracts\Voting.json") as f:
            contract_data = json.load(f)

        network_ids = list(contract_data['networks'].keys())
        latest_network_id = max(network_ids, key=int)

        self.contract_address = contract_data['networks'][latest_network_id]['address']
        self.abi = contract_data['abi']
        self.contract = self.w3.eth.contract(address=self.contract_address, abi=self.abi)

        candidates = self.db.fetch_candidate()
        for candidate_id, candidate_info in candidates.items():
            # print(candidate_id,candidate_info["party"],candidate_info["name"])
            self.add_candidate(candidate_id,candidate_info["party"],candidate_info["name"])

    # Function to add a candidate
    def add_candidate(self, candidate_id, party_name, candidate_name):
        try:
            tx_hash = self.contract.functions.addCandidate(candidate_id, party_name, candidate_name).transact({
                'from': self.w3.eth.defaultAccount
            })
            self.w3.eth.wait_for_transaction_receipt(tx_hash)
            print(f"Candidate {candidate_name} added with ID {candidate_id}.")
        except ContractLogicError as e:
            if "Candidate ID already exists" in str(e):
                print("False")  # Print "False" if candidate ID already exists
            else:
                print("Error:", e)  # Print other errors if any

    # Function to check if voter has voted
    def has_voted(self, aadhaar):
        try:
            voted = self.contract.functions.checkIfVoted(aadhaar).call()
            if not voted:
                return False  # Explicitly print "False" if the user has not voted
            else:
                return True
        except:
            return False

    # Function to vote
    def vote(self, candidate_id, aadhaar):
        if self.has_voted(aadhaar):
            print("You have already voted.")
            return False
        tx_hash = self.contract.functions.vote(candidate_id, aadhaar).transact({
            'from': self.w3.eth.defaultAccount
        })
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Voted for candidate {candidate_id}.")
        return True


    # Function to get results
    def get_results(self):
        results = self.contract.functions.getResults().call()
        return results

# Example Usage
if __name__ == "__main__":
    # # Replace the contract JSON path with your actual path
    voting_system = VotingSystem()

    # Add candidates with custom IDs
    # voting_system.add_candidate(1, "Party A", "Alice")
    # voting_system.add_candidate(2, "Party B", "Bob")
    
    # # Voting example
    # voting_system.vote("c001", "123456789018")  # Voting for candidate with custom ID 1

    # print(voting_system.has_voted("123456789018"))
    
    # # # Get results
    # voting_system.get_results()
    pass