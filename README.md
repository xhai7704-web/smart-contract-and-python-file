DS441 A – BLOCKCHAIN: THEORY & PRACTICES

INDIVIDUAL MINI PROJECT: CROWDFUNDING CAMPAIGN

STUDENT INFORMATION

* Full Name: Dương Xuân Hải
* Student ID: 28211102398
* Course: DS 441 A – Blockchain: Theory & Practices
* Project: Crowdfunding Campaign

⸻

1. PROJECT DESCRIPTION

This project implements a Crowdfunding Campaign using Solidity Smart Contracts and Python Web3.

The campaign has a funding goal and a deadline. Contributors can send ETH before the deadline.

After the deadline:

* If the funding goal is reached, the campaign owner can withdraw the funds.
* If the funding goal is not reached, contributors can claim refunds.
* Each contributor can claim a refund only once.

2. TECHNOLOGIES USED

* Solidity 0.8.20
* Ganache
* Python 3
* Web3.py
* Remix IDE

3. MAIN FEATURES

* Create a crowdfunding campaign with a funding goal.
* Set a campaign deadline.
* Accept ETH contributions before the deadline.
* Allow the owner to withdraw funds if the goal is reached.
* Allow contributors to claim refunds if the campaign fails.
* Prevent duplicate refund requests.
* Emit events for contributions, withdrawals, and refunds.

4. PROJECT STRUCTURE

DS441-Crowdfunding-Campaign/
│
├── CrowdfundingCampaign.sol
├── crowdfunding_client.py
├── README.md
└── requirements.txt

5. INSTALLATION

Step 1: Start Ganache

Start Ganache and create a local blockchain.

Default RPC URL:

http://127.0.0.1:7545

Use Ganache test accounts and test ETH only.

Step 2: Install Python dependencies

Create a virtual environment:

python -m venv .venv

Install required libraries:

pip install -r requirements.txt

6. SMART CONTRACT DEPLOYMENT

1. Open Remix IDE: https://remix.ethereum.org/
2. Create a file named CrowdfundingCampaign.sol.
3. Copy the Solidity source code into Remix.
4. Select Solidity compiler version 0.8.20 or compatible.
5. Compile the contract.
6. Connect Remix to the Ganache blockchain using a test wallet configured for Ganache.
7. Select CrowdfundingCampaign.
8. Enter the constructor parameters:
    * Funding Goal: 1000000000000000000 Wei (1 ETH).
    * Duration: 300 seconds.
9. Deploy the contract.
10. Copy the deployed contract address.

7. PYTHON CONFIGURATION

Open crowdfunding_client.py.

Update the following configuration:

RPC_URL = "http://127.0.0.1:7545"
CONTRACT_ADDRESS = "YOUR_DEPLOYED_CONTRACT_ADDRESS"

Replace the contract address with your actual deployed contract address.

Run the Python application:

python crowdfunding_client.py

8. TESTING SCENARIOS

Test Case 1: Successful Campaign

1. Deploy a campaign with a goal of 1 ETH.
2. Account 1 contributes 0.6 ETH.
3. Account 2 contributes 0.4 ETH.
4. Wait until the deadline.
5. The campaign owner withdraws the funds.

Expected result:

* Total contributions reach 1 ETH.
* The owner can withdraw the funds.
* A second withdrawal is rejected.

Test Case 2: Failed Campaign

1. Deploy a new campaign with a goal of 1 ETH.
2. Account 1 contributes 0.2 ETH.
3. Account 2 contributes 0.3 ETH.
4. Wait until the deadline.
5. The owner attempts to withdraw funds.
6. Contributors claim their refunds.

Expected result:

* Total contributions are below 1 ETH.
* The owner’s withdrawal is rejected.
* Contributors can receive their refunds.
* A second refund request is rejected.

9. IMPORTANT NOTES

* All transactions are performed on a local Ganache blockchain.
* Only test Ether is used.
* The deployed contract address must match the active Ganache network.
* Each campaign requires a separate contract deployment.
* Test results and screenshots should be added after actual execution.

10. PROJECT AUTHOR

Dương Xuân Hải
Student ID: 28211102398

Course: DS 441 A – Blockchain: Theory & Practices

Source code and documentation were prepared with assistance from ChatGPT. The student should deploy, test, verify, and understand the implementation before submission.
