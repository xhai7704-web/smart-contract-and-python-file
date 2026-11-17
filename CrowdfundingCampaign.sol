// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title Crowdfunding Campaign - DS441 Individual Mini Project
/// @author Duong Xuan Hai - 28211102398
contract CrowdfundingCampaign {
    address public immutable owner;
    uint256 public immutable fundingGoal;
    uint256 public immutable deadline;

    uint256 public totalRaised;
    bool public withdrawn;

    mapping(address => uint256) public contributions;
    mapping(address => bool) public hasRefunded;

    event ContributionReceived(address indexed contributor, uint256 amount, uint256 totalRaised);
    event FundsWithdrawn(address indexed owner, uint256 amount);
    event RefundClaimed(address indexed contributor, uint256 amount);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only campaign owner");
        _;
    }

    constructor(uint256 _fundingGoalWei, uint256 _durationSeconds) {
        require(_fundingGoalWei > 0, "Funding goal must be greater than zero");
        require(_durationSeconds > 0, "Duration must be greater than zero");

        owner = msg.sender;
        fundingGoal = _fundingGoalWei;
        deadline = block.timestamp + _durationSeconds;
    }

    /// @notice Anyone may contribute while the campaign is still active.
    function contribute() external payable {
        require(block.timestamp < deadline, "Campaign has ended");
        require(msg.value > 0, "Contribution must be greater than zero");

        contributions[msg.sender] += msg.value;
        totalRaised += msg.value;

        emit ContributionReceived(msg.sender, msg.value, totalRaised);
    }

    /// @notice The owner may withdraw once, after the deadline, if the goal was met.
    function withdrawFunds() external onlyOwner {
        require(block.timestamp >= deadline, "Campaign is still active");
        require(totalRaised >= fundingGoal, "Funding goal was not met");
        require(!withdrawn, "Funds already withdrawn");

        withdrawn = true;
        uint256 amount = address(this).balance;

        (bool success, ) = payable(owner).call{value: amount}("");
        require(success, "Transfer failed");

        emit FundsWithdrawn(owner, amount);
    }

    /// @notice A contributor may claim their full contribution once if the goal failed.
    function claimRefund() external {
        require(block.timestamp >= deadline, "Campaign is still active");
        require(totalRaised < fundingGoal, "Funding goal was met");
        require(!hasRefunded[msg.sender], "Refund already claimed");

        uint256 amount = contributions[msg.sender];
        require(amount > 0, "No contribution to refund");

        hasRefunded[msg.sender] = true;
        contributions[msg.sender] = 0;

        (bool success, ) = payable(msg.sender).call{value: amount}("");
        require(success, "Refund transfer failed");

        emit RefundClaimed(msg.sender, amount);
    }

    function getCampaignStatus()
        external
        view
        returns (
            uint256 goal,
            uint256 raised,
            uint256 campaignDeadline,
            uint256 remainingSeconds,
            bool goalReached,
            bool campaignEnded,
            bool fundsWithdrawn
        )
    {
        goal = fundingGoal;
        raised = totalRaised;
        campaignDeadline = deadline;
        remainingSeconds = block.timestamp < deadline ? deadline - block.timestamp : 0;
        goalReached = totalRaised >= fundingGoal;
        campaignEnded = block.timestamp >= deadline;
        fundsWithdrawn = withdrawn;
    }
}
