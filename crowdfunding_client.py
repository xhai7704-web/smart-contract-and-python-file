"""
DS441 A - Blockchain: Theory & Practices
Individual Mini Project: Crowdfunding Campaign
Student: Duong Xuan Hai | Student ID: 28211102398

Prerequisites:
    pip install "web3>=6,<8"

Run:
    python crowdfunding_client.py

Start Ganache first (default RPC: http://127.0.0.1:7545).
Deploy CrowdfundingCampaign.sol, then paste the deployed address below.
Use only Ganache test accounts and test ETH.
"""

from web3 import Web3
from datetime import datetime, timezone

RPC_URL = "http://127.0.0.1:7545"
CONTRACT_ADDRESS = "PASTE_DEPLOYED_CONTRACT_ADDRESS_HERE"

# ABI for CrowdfundingCampaign.sol
ABI = [
    {
        "inputs": [
            {"internalType": "uint256", "name": "_fundingGoalWei", "type": "uint256"},
            {"internalType": "uint256", "name": "_durationSeconds", "type": "uint256"}
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "contributor", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "totalRaised", "type": "uint256"}
        ],
        "name": "ContributionReceived",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "owner", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"}
        ],
        "name": "FundsWithdrawn",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "contributor", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"}
        ],
        "name": "RefundClaimed",
        "type": "event"
    },
    {
        "inputs": [],
        "name": "claimRefund",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "contribute",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "", "type": "address"}],
        "name": "contributions",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "deadline",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "fundingGoal",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getCampaignStatus",
        "outputs": [
            {"internalType": "uint256", "name": "goal", "type": "uint256"},
            {"internalType": "uint256", "name": "raised", "type": "uint256"},
            {"internalType": "uint256", "name": "campaignDeadline", "type": "uint256"},
            {"internalType": "uint256", "name": "remainingSeconds", "type": "uint256"},
            {"internalType": "bool", "name": "goalReached", "type": "bool"},
            {"internalType": "bool", "name": "campaignEnded", "type": "bool"},
            {"internalType": "bool", "name": "fundsWithdrawn", "type": "bool"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "", "type": "address"}],
        "name": "hasRefunded",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "totalRaised",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "withdrawFunds",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "withdrawn",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    }
]


def connect():
    """Connect to Ganache and validate the deployed contract."""
    w3 = Web3(Web3.HTTPProvider(RPC_URL, request_kwargs={"timeout": 10}))
    if not w3.is_connected():
        raise ConnectionError(
            f"Cannot connect to Ganache at {RPC_URL}. "
            "Please start Ganache and check the RPC URL."
        )

    if not Web3.is_address(CONTRACT_ADDRESS):
        raise ValueError("Please set CONTRACT_ADDRESS to the deployed contract address.")

    address = Web3.to_checksum_address(CONTRACT_ADDRESS)
    if not w3.eth.get_code(address):
        raise ValueError(
            "No contract code at this address. Check the address and selected Ganache network."
        )

    contract = w3.eth.contract(address=address, abi=ABI)
    accounts = w3.eth.accounts
    if not accounts:
        raise RuntimeError("Ganache returned no unlocked accounts.")

    print("\nConnected to Ganache")
    print("Chain ID:", w3.eth.chain_id)
    print("Contract:", address)
    print("Accounts available:", len(accounts))
    return w3, contract, accounts


def choose_account(accounts):
    print("\nGanache accounts:")
    for index, account in enumerate(accounts):
        print(f"  {index}: {account}")
    while True:
        try:
            index = int(input("Choose account index: ").strip())
            if 0 <= index < len(accounts):
                return accounts[index]
        except ValueError:
            pass
        print("Invalid selection. Please enter a valid account index.")


def show_status(w3, contract, account):
    status = contract.functions.getCampaignStatus().call()
    goal, raised, deadline, remaining, reached, ended, withdrawn = status

    print("\n========== CAMPAIGN STATUS ==========")
    print("Owner:              ", contract.functions.owner().call())
    print("Connected account:  ", account)
    print("Funding goal:       ", Web3.from_wei(goal, "ether"), "ETH")
    print("Total raised:       ", Web3.from_wei(raised, "ether"), "ETH")
    print("Contract balance:   ", Web3.from_wei(
        w3.eth.get_balance(contract.address), "ether"), "ETH")
    print("Deadline:           ", datetime.fromtimestamp(
        deadline, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"))
    print("Seconds remaining:  ", remaining)
    print("Goal reached:       ", reached)
    print("Campaign ended:     ", ended)
    print("Funds withdrawn:    ", withdrawn)
    print("Your contribution:  ", Web3.from_wei(
        contract.functions.contributions(account).call(), "ether"), "ETH")
    print("Already refunded:   ", contract.functions.hasRefunded(account).call())
    print("=====================================")


def send_transaction(w3, function_call, account, value=0):
    """Send a transaction from an unlocked Ganache account and show its result."""
    try:
        tx_hash = function_call.transact({
            "from": account,
            "value": value,
            "gas": 500000
        })
        print("Transaction sent:", tx_hash.hex())
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            print("SUCCESS - block:", receipt.blockNumber)
            print("Gas used:", receipt.gasUsed)
            return receipt
        print("FAILED - transaction reverted.")
    except Exception as error:
        print("\nTRANSACTION REJECTED:")
        print(str(error))


def main():
    try:
        w3, contract, accounts = connect()
    except Exception as error:
        print("Connection/setup error:", error)
        return

    account = choose_account(accounts)

    while True:
        print("\n========== CROWDFUNDING MENU ==========")
        print("1. Show campaign status")
        print("2. Contribute ETH")
        print("3. Withdraw funds (campaign owner only)")
        print("4. Claim refund (failed campaign only)")
        print("5. Switch Ganache account")
        print("0. Exit")
        choice = input("Select: ").strip()

        if choice == "1":
            show_status(w3, contract, account)

        elif choice == "2":
            try:
                amount = float(input("Contribution amount (ETH): ").strip())
                if amount <= 0:
                    print("Amount must be greater than zero.")
                    continue
                value = Web3.to_wei(amount, "ether")
                send_transaction(w3, contract.functions.contribute(), account, value)
            except ValueError:
                print("Please enter a valid numeric ETH amount.")

        elif choice == "3":
            send_transaction(w3, contract.functions.withdrawFunds(), account)

        elif choice == "4":
            send_transaction(w3, contract.functions.claimRefund(), account)

        elif choice == "5":
            account = choose_account(accounts)
            print("Connected account changed to:", account)

        elif choice == "0":
            print("Goodbye.")
            break

        else:
            print("Invalid option. Choose 0, 1, 2, 3, 4, or 5.")


if __name__ == "__main__":
    main()
