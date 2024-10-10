import base64
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

class BlockchainClient:
    def __init__(self, network="testnet"):
        self.network = network
        self.algod_client = None
        self.indexer_client = None
        self.setup_clients()

    def setup_clients(self):
        """Initialize Algod and Indexer clients based on the selected network."""
        try:
            if self.network == "localnet":
                print("Localnet client created!!!")
                algod_address_local = "http://localhost:4001"
                algod_token = "a" * 64
                self.algod_client = AlgodClient(algod_token, algod_address_local)
                indexer_localnet_url = "http://localhost:8980"
                self.indexer_client = IndexerClient("", indexer_localnet_url)

            elif self.network == "testnet":
                print("Testnet client created!!!")
                algod_address_testnet = "https://testnet-api.algonode.cloud"
                algod_token = "a" * 64
                self.algod_client = AlgodClient(algod_token, algod_address_testnet)
                indexer_url_testnet = "https://testnet-idx.algonode.cloud"
                self.indexer_client = IndexerClient("", indexer_url_testnet)

            elif self.network == "mainnet":
                print("Mainnet functionalities are yet to be implemented!!!")
                raise Exception("Mainnet not implemented yet!!!")

            else:
                print("Please select either 'localnet' or 'testnet'")
                raise Exception("Invalid network name!!!")

        except Exception as e:
            print(f"Error in setting up clients: {e}")

    def fetch_all_transactions(self, address):
        """Fetch all transactions for a given address."""
        try:
            response = self.indexer_client.search_transactions(address=address)
            transactions = response["transactions"]

            all_transaction_details = {}

            # Decode transaction attributes
            for txn in transactions:
                global_state_delta = txn.get('global-state-delta')
                if global_state_delta:
                    for delta in global_state_delta:
                        attribute = delta.get('key')
                        value = delta.get('value').get('bytes')

                        decoded_attribute = base64.b64decode(attribute).decode('utf-8')
                        decoded_value = base64.b64decode(value).decode('utf-8')

                        if decoded_attribute not in all_transaction_details:
                            all_transaction_details[decoded_attribute] = []
                        all_transaction_details[decoded_attribute].append(decoded_value)

            return all_transaction_details
        except Exception as e:
            print(f"Error occurred: {e}")
            return None

    def fetch_latest_transaction_string(self,app_id):
        """Fetch the latest transaction for a APP ID stored as Integer ."""


        latest_transaction = {}
        try:
            response = self.indexer_client.search_transactions(application_id=app_id)
            transactions = response["transactions"][-1]

            global_state_delta = transactions.get("global-state-delta" , "NAN")


            if global_state_delta != "NAN":
                for single_delta in global_state_delta:
                    attribute = single_delta.get("key")
                    decoded_attribute = base64.b64decode(attribute.encode()).decode("utf-8")
                    value = single_delta['value']['bytes']
                    decoded_value = base64.b64decode(value.encode()).decode("utf-8")
                    latest_transaction[decoded_attribute] = decoded_value
                return latest_transaction
            else:
                print("Global storage empty ")
                return {}

        except Exception as e:
            print(f"Error occurred: {e}")
            return {}

    def fetch_latest_transaction_integer(self,app_id):
        """Fetch the latest transaction for a APP ID stored as Integer ."""


        latest_transaction = {}
        try:
            response = self.indexer_client.search_transactions(application_id=app_id)
            transactions = response["transactions"][-1]

            global_state_delta = transactions.get("global-state-delta" , "NAN")


            if global_state_delta != "NAN":
                for single_delta in global_state_delta:
                    attribute = single_delta.get("key")
                    decoded_attribute = base64.b64decode(attribute.encode()).decode("utf-8")
                    value = single_delta['value']['uint']
                    latest_transaction[decoded_attribute] = value
                return latest_transaction
            else:
                print("Global storage empty ")
                return {}

        except Exception as e:
            print(f"Error occurred: {e}")
            return {}
        

    
        
    def filter_response_only(self, response):
        """Filter blockchain response for a particular transaction."""
        try:
            blockchain_data = {}
            blockchain_data["applicationid"] = response.tx_info["txn"]["txn"]["apid"]
            blockchain_data["gasfees"] = response.tx_info["txn"]["txn"]["fee"]
            blockchain_data["transactionid"] = response.tx_id
            blockchain_data["walletaddress"] = response.tx_info['txn']['txn']['snd']
            blockchain_data["blocknumber"] = response.confirmed_round

            # Fetch block info from the client
            block_info = self.algod_client.block_info(blockchain_data["blocknumber"])
            blockchain_data["blocktimestamp"] = block_info["block"]["ts"]

            return blockchain_data
        except Exception as e:
            print(f"Error occurred while filtering response: {e}")
            return None


# Example usage
if __name__ == "__main__":
    address = "your-wallet-address"
    
    # Initialize client for the testnet
    client = BlockchainClient(network="testnet")

    # Fetch all transactions for an address
    all_transactions = client.fetch_all_transactions(address)
    print("All Transactions: ", all_transactions)

    # Fetch latest transaction
    latest_transaction = client.fetch_latest_transaction(address)
    print("Latest Transaction: ", latest_transaction)

    # Filter a sample response (replace 'response' with actual response data)
    # response = your_response_data
    # filtered_data = client.filter_response_only(response)
    # print("Filtered Transaction Data: ", filtered_data)
