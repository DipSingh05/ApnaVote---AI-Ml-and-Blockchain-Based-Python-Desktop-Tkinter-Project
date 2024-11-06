// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Voting {
    struct Candidate {
        string partyName;
        string candidateName;
        uint256 votes;
    }

    mapping(bytes32 => Candidate) public candidates; // Use bytes32 as key
    mapping(bytes32 => bool) public hasVoted;        // Tracks if a voter has voted
    bytes32[] public candidateIds;                   // Store candidate IDs for retrieval

    // Event to log results
    event VoteCasted(bytes32 indexed candidateId, uint256 votes);
    
    // Function to add a candidate with a custom ID
    function addCandidate(string memory candidateId, string memory _partyName, string memory _candidateName) public {
        bytes32 candidateKey = keccak256(abi.encodePacked(candidateId));  // Hash candidate ID
        require(bytes(candidates[candidateKey].candidateName).length == 0, "Candidate ID already exists.");

        // Add the candidate to the mapping
        candidates[candidateKey] = Candidate(_partyName, _candidateName, 0);
        candidateIds.push(candidateKey);  // Add the candidate ID to the list
    }

    // Voting function with Aadhaar ID check
    function vote(string memory candidateId, string memory aadhaar) public {
        bytes32 candidateKey = keccak256(abi.encodePacked(candidateId)); // Hash candidate ID
        bytes32 aadhaarHash = keccak256(abi.encodePacked(aadhaar));      // Hash Aadhaar ID
        require(bytes(candidates[candidateKey].candidateName).length > 0, "Candidate does not exist.");
        require(!hasVoted[aadhaarHash], "You have already voted.");      // Check if the voter has already voted
        
        hasVoted[aadhaarHash] = true;  // Mark the voter as having voted
        candidates[candidateKey].votes++;
        
        emit VoteCasted(candidateKey, candidates[candidateKey].votes);
    }

    // Function to get vote results for all candidates
    function getResults() public view returns (Candidate[] memory) {
        Candidate[] memory result = new Candidate[](candidateIds.length);
        for (uint256 i = 0; i < candidateIds.length; i++) {
            result[i] = candidates[candidateIds[i]];
        }
        return result;
    }

    // Function to check if a voter has voted
    function checkIfVoted(string memory aadhaar) public view returns (bool) {
        bytes32 aadhaarHash = keccak256(abi.encodePacked(aadhaar));
        return hasVoted[aadhaarHash];  // Return whether the voter has voted
    }

    // Function to get candidate IDs (for frontend or other applications)
    function getCandidateIds() public view returns (bytes32[] memory) {
        return candidateIds;
    }
}
