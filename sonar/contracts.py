import textwrap,json,zlib,copy,pickle,math,codecs
import multihash,ipfsapi
from solc import compile_source, compile_files, link_code
from web3 import Web3, KeepAliveRPCProvider
from os.path import isfile, join
from os import listdir

class Gradient():
    def __init__(self, owner, grad_values):
        self.owner = owner
        self.grad_values = grad_values

class Model():

    def __init__(self, owner, syft_obj, bounty, initial_error, target_error, model_id=None, repo=None):
        self.owner = owner
        self.syft_obj = syft_obj
        self.bounty = bounty
        self.initial_error = initial_error
        self.target_error = target_error
        self.model_id = model_id
        self.repo = repo

    def __getitem__(self,gradient_id):
        (grad_owner, mca) = self.repo.call.getGradient(self.model_id,gradient_id)
        grad_values = self.repo.ipfs.get_pyobj(str(mca[0]+mca[1]).split("\x00")[0])
        g = Gradient(grad_owner,grad_values)
        return g

    def generate_gradient(self,input,target):
        return self.syft_obj.generate_gradient(input,target)

    def __str__(self):
        s = ""
        s += "Desc:" + str(self.syft_obj.desc) + "\n"
        s += "Owner:" + str(self.owner) + "\n"
        s += "Bounty:" + str(self.bounty) + "\n"
        s += "Initial Error:" + str(self.initial_error) + "\n"
        s += "Target Error:" + str(self.target_error) + "\n"
        s += "Model ID:" + str(self.model_id) + "\n"
        return s

    def __repr__(self):
        s = ""
        s += "Desc:" + str(self.syft_obj.desc) + "\n"
        s += "Owner:" + str(self.owner) + "\n"
        s += "Bounty:" + str(self.bounty) + "\n"
        s += "Initial Error:" + str(self.initial_error) + "\n"
        s += "Target Error:" + str(self.target_error) + "\n"
        s += "Model ID:" + str(self.model_id) + "\n"
        return s





class ModelRepository():
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

        if(account is not None):
            self.account = account
        else:
            print("No account submitted... using default[2]")
            self.account = self.web3.eth.accounts[2]

        self.compile_and_deploy()

        print("Deployed ModelRepository:" + str(self.deploy_txn))

    def compile_and_deploy(self,directory='contracts/'):
        """This contract selects the contract associated with this python interface
        compiles it, and deploys it to a locally hosted (testrpc) blockchain."""

        f = open('../contracts/ModelRepository.sol','r')
        source = f.read()
        f.close()

        compiled = compile_source(source)['<stdin>:ModelRepository']

        self.contract = self.web3.eth.contract(
            abi = compiled['abi'],
            bytecode = compiled['bin'],
            bytecode_runtime = compiled['bin-runtime'],
            source = source,
            )

        if(self.deploy_txn is None):
            self.deploy_txn = self.contract.deploy({'from': self.account})

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

    def submit_model(self,model):
        """This accepts a model from syft.nn, loads it into IPFS, and uploads
        the IPFS address to the blockchain.

        TODO: use best practices for storing IPFS addresses on the blockchain.

        """

        ipfs_address = self.ipfs.add_pyobj(model.syft_obj)
        deploy_trans = self.get_transaction(model.owner,value=self.web3.toWei(model.bounty,'ether')).addModel([ipfs_address[0:32],ipfs_address[32:]],model.initial_error,model.target_error)
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

            (owner,bounty, initial_error, target_error, mca) = self.call.getModel(model_id)
            syft_obj = self.ipfs.get_pyobj(str(mca[0]+mca[1]).split("\x00")[0])
            model = Model(owner,syft_obj,self.web3.fromWei(bounty,'ether'),initial_error,target_error,model_id,self)

            return model

    def __len__(self):
        return self.call.getNumModels()
