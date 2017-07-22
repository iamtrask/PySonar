import textwrap,json,zlib,copy,pickle,math,codecs
import multihash,ipfsapi
from solc import compile_source, compile_files, link_code
from web3 import Web3, KeepAliveRPCProvider
from os.path import isfile, join
from os import listdir

class ModelMine():
    """This class is a python client wrapper around the ModelMine.sol contract,
    giving easy to use python functions around the contract's functionality. It
    currently assumes you're running on a local testrpc Ethereum blockchain."""

    def __init__(self,account=None,deploy_txn=None,web3_port=8545,ipfs_port=5001):
        """Creates the base blockchain client object (web3), ipfs client object (ipfs),
        and deploys the compiled contract. Thus, it assumes that you're working with a
        local testrpc blockchain."""


        self.deploy_txn = deploy_txn
        self.web3 = Web3(KeepAliveRPCProvider(host='localhost', port=str(web3_port)))
        self.ipfs = ipfsapi.connect('127.0.0.1', int(ipfs_port))

        self.compile_and_deploy()
        if(account is not None):
            self.account = account
        else:
            print("No account submitted... using default[2]")
            self.account = self.web3.eth.accounts[2]

    def compile_and_deploy(self,directory='contracts/'):
        """This contract selects the contract associated with this python interface
        compiles it, and deploys it to a locally hosted (testrpc) blockchain."""

        f = open('../contracts/ModelMine.sol','r')
        source = f.read()
        f.close()

        compiled = compile_source(source)['<stdin>:ModelMine']

        self.contract = self.web3.eth.contract(
            abi = compiled['abi'],
            bytecode = compiled['bin'],
            bytecode_runtime = compiled['bin-runtime'],
            source = source,
            )

        if(self.deploy_txn is None):
            self.deploy_txn = self.contract.deploy()
        txn_receipt = self.web3.eth.getTransactionReceipt(self.deploy_txn)
        self.contract_address = txn_receipt['contractAddress']

        self.call = self.contract.call({
            "from":self.web3.eth.accounts[2],
            "to":self.contract_address,
            })

        return self.deploy_txn

    def get_transaction(self,from_addr,value=None):
        """I consistently forget the conventions for executing transactions against
        compiled contracts. This function helps that to be easier for me."""

        txn = {}
        txn["from"] = from_addr
        txn["to"] = self.contract_address

        if(value is not None):
            txn["value"] = int(value)

        transact_raw = self.contract.transact(txn)
        return transact_raw

    def submit_model(self,from_addr,model,bounty,initial_error,target_error):
        """This accepts a model from syft.nn, loads it into IPFS, and uploads
        the IPFS address to the blockchain.

        TODO: use best practices for storing IPFS addresses on the blockchain.

        """

        ipfs_address = self.ipfs.add_pyobj(model)
        deploy_trans = self.get_transaction(from_addr,value=self.web3.toWei(bounty,'ether')).addModel([ipfs_address[0:32],ipfs_address[32:]],initial_error,target_error)
        return self.call.getNumModels()-1

    def submit_gradient(self,from_addr,model_id,grad):
        """This accepts gradients for a model from syft.nn and uploads them to
        the blockchain (via IPFS), linked to a model by it's id.

        TODO: modify syft.nn to actually have a "getGradients()" method call so
        that there can be checks that keep people from uploading junk. Currently
        any python object could be uploaded (which is obviously dangerous)."""

        ipfs_address = self.ipfs.add_pyobj(grad)
        deploy_trans = self.get_transaction(from_addr).addGradient(model_id,[ipfs_address[0:32],ipfs_address[32:]])
        return self.call.getNumGradientsforModel(model_id)-1

    def __getitem__(self,model_id):
        if(model_id < len(self)):
            mca = self.call.getModel(model_id)
            model_client = self.ipfs.get_pyobj(str(mca[0]+mca[1]).split("\x00")[0])
            return model_client

    def __len__(self):
        return self.call.getNumModels()
