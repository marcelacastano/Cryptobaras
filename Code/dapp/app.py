from decimal import Decimal
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from datetime import datetime
# from bip44 import Wallet
from web3.gas_strategies.time_based import medium_gas_price_strategy
from web3.middleware import geth_poa_middleware


load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider('https://rinkeby.infura.io/v3/ae97deb9bbb14f0499e857aa136e10ad'))


# Set page configuration
st.set_page_config(page_title="CryptoBaras Minter", page_icon="🆕")

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################

# Cache the contract on load
@st.cache(allow_output_mutation=True)
# Define the load_contract function
def load_contract():

    # Load Art Gallery ABI
    with open(Path('./contract_abi.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = "0xd843D6E8ce84f890Bb88F79b8aECE519e41657e5"

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )
    # Return the contract from the function
    return contract


# Load the contract
contract = load_contract()


################################################################################
# Mint NFT
################################################################################

# Set title
st.markdown("# CRYPTOBARAS MINTER")

# Set page banner
st.image('images/preview.gif')
st.markdown("---")

# Interact with contract
st.markdown("## There's only 100 CryptoBaras in Existence")

st.markdown("Check how many are left for you to mint:")

if st.button("Check Available"):
    total_supply = contract.functions.totalSupply().call()
    token_list = st.write(100-total_supply)

st.markdown("## How Much does a CryptoBara Cost?")
st.markdown("Click on Cost to retrieve the price of a CryptoBara in **Wei**:")

if st.button("Cost"):
    cost = contract.functions.cost().call()
    st.write(cost)

# Make a transaction
st.markdown("## Mint Your Own CryptoBara!")
mintAmount = st.number_input("You Can Mint Up to 5 CryptoBaras", max_value=5, min_value=1)
print(mintAmount, datetime.now())

# Enter the purchaser's (To) wallet address
minter_address = st.text_input("Enter Rinkeby Address")
print("Minting to wallet address: " + minter_address, datetime.now())

# Enter contract owner's wallet address
contractowner_address = "0x24E8C8f8DA11aeD86b87fd72de1b3203233c50BD"
contractowner_private_key = os.getenv("METAMASK_ACCOUNT2_PRIVATE_KEY")

# Build the transaction
# Get Gas Estimate
value = w3.toWei(0.02,'ether')
w3.eth.setGasPriceStrategy(medium_gas_price_strategy)

# Get the nonce
nonce = w3.eth.get_transaction_count(contractowner_address)
print("Nonce:", nonce, datetime.now())

# Middleware
w3.middleware_onion.inject(geth_poa_middleware, layer=0)


# Mint Button
if st.button("Mint"):
    
    value = value*mintAmount
    if minter_address == contractowner_address:
        value = 0

    transaction = {
        "from": contractowner_address,
        "gas": 3000000,
        "gasPrice": w3.eth.generate_gas_price(),
        "value": value,
        "nonce": nonce
    }

    print(datetime.now(), "line 122")
    transaction_build = contract.functions.mint(mintAmount, minter_address).buildTransaction(transaction)
    print(datetime.now(), "line 123")
    signed_tx = w3.eth.account.sign_transaction(transaction_build, contractowner_private_key)
    print(datetime.now(), "line 125")
    txn_raw = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(datetime.now(), "line 127")
    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_raw)
    print(datetime.now(), "line 129")
    print(dict(txn_receipt))

    st.write("Transaction receipt mined:")
    st.write(dict(txn_receipt))


# Hide Streamlit Style
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
