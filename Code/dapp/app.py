# Imports
##################################################################################
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from datetime import datetime
from web3.gas_strategies.time_based import medium_gas_price_strategy
from web3.middleware import geth_poa_middleware

# Initial Configurations
#################################################################################

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

# Set streamlit page configuration
st.set_page_config(page_title="CryptoBaras Minter", page_icon="🪙")



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
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )
    # Return the contract from the function
    return contract


# Load the contract
contract = load_contract()


# User-Friendly Interface
################################################################################

# Set title
title = '<h1 style="font-family:Freestyle Script; font-size: 130px;"><center>CryptoBaras Minter</center></p>'
st.markdown(title, unsafe_allow_html=True)

# Set page banner
st.image('images/preview.gif')
st.markdown("---")

# Interact with contract
##########################
st.markdown("## There's only 100 CryptoBaras in Existence")

st.markdown("Check how many are left for you to mint:")

if st.button("Check Available"):
    total_supply = contract.functions.totalSupply().call()
    token_list = st.write(100-total_supply)

st.markdown("## How Much Does a CryptoBara Cost?")
st.markdown("Click on **Cost** to retrieve the price of a CryptoBara in **Wei**:")

if st.button("Cost"):
    cost = contract.functions.cost().call()
    st.write(cost)

st.markdown("---")

# Make a transaction
###########################

st.markdown("## Mint Your Own CryptoBara")
mintAmount = 1

# Enter the purchaser's (To) wallet address
minter_address = st.text_input("Enter Rinkeby Address")

# Enter contract owner's wallet address
contractowner_address = str(os.getenv("CONTRACT_OWNER_ADDRESS"))
contractowner_private_key = os.getenv("CONTRACT_OWNER_PRIVATE_KEY")

# Get Gas Estimate
value = w3.toWei(0.02,'ether')
w3.eth.setGasPriceStrategy(medium_gas_price_strategy)

# Get the nonce
nonce = w3.eth.get_transaction_count(contractowner_address)

# Middleware
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Mint Button
if st.button("Mint"):

    # Show loading widget
    with st.spinner(text='Wait for it...'):
    
        value = value*mintAmount
        if minter_address == contractowner_address:
            value = 0

        print(datetime.now(), "Amount: ", mintAmount, " Nonce:", nonce, " Minting to wallet: ", minter_address)

        transaction = {
            "from": contractowner_address,
            "gas": 3000000,
            "gasPrice": w3.eth.generate_gas_price(),
            "value": value,
            "nonce": nonce
        }

        # Build the transaction
        transaction_build = contract.functions.mint(mintAmount, minter_address).buildTransaction(transaction)
        print(datetime.now(), "transaction built")

        # Sign transaction
        signed_tx = w3.eth.account.sign_transaction(transaction_build, contractowner_private_key)
        print(datetime.now(), "transaction signed")

        # Send transaction
        txn_raw = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(datetime.now(), "raw transaction sent")

        # Obtain transaction receipt
        txn_receipt = w3.eth.wait_for_transaction_receipt(txn_raw)
        print(dict(txn_receipt))

    # Show receipt to user
    st.success('Done')
    st.balloons()
    st.write("Transaction receipt mined:")
    st.write(dict(txn_receipt))

st.markdown("---")


# See Token URI
#########################

st.markdown("## Take a Look at Your Tokens")

st.markdown("Enter Owner Address and Hit the **Check Tokens** button to retrieve TokenIds for all of your CryptoBaras:")

minter_address = st.text_input("Owner Address")

if st.button("Check Tokens"):
    tokens_by_owner = contract.functions.walletOfOwner(minter_address).call()
    st.write("Tokens You Own:", tokens_by_owner)


token_id = st.text_input("Enter TokenID You'd Like to See:")
contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

if st.button("See Token"):
    st.markdown(f"Here's the link to your CryptoBara on [Open Sea](https://testnets.opensea.io/assets/{contract_address}/{token_id}/)")


# Hide Streamlit Style
#################################################################################
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)