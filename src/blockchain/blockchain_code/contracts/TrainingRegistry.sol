// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TrainingRegistry {
    
    struct TrainingRecord {
        uint256 round;
        string modelHash;
        uint256 accuracy; 
        uint256 loss;     
        uint256 timestamp;
    }

    mapping(address => TrainingRecord[]) public history;
    address[] public clients;
    mapping(address => bool) isRegistered;

    event RecordAdded(address indexed client, uint256 round, uint256 accuracy);

    function recordTraining(
        uint256 _round,
        string memory _modelHash,
        uint256 _accuracy,
        uint256 _loss
    ) public {
        if (!isRegistered[msg.sender]) {
            isRegistered[msg.sender] = true;
            clients.push(msg.sender);
        }

        TrainingRecord memory newRecord = TrainingRecord({
            round: _round,
            modelHash: _modelHash,
            accuracy: _accuracy,
            loss: _loss,
            timestamp: block.timestamp
        });

        history[msg.sender].push(newRecord);
        emit RecordAdded(msg.sender, _round, _accuracy);
    }

    function getHistoryCount(address _client) public view returns (uint256) {
        return history[_client].length;
    }

    function getAllClients() public view returns (address[] memory) {
        return clients;
    }
}