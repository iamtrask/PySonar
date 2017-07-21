import textwrap,json,zlib,copy,pickle,math,codecs
import multihash,ipfsapi
from solc import compile_source, compile_files, link_code
from web3 import Web3, KeepAliveRPCProvider
from os.path import isfile, join
from os import listdir

class ModelMine():

    def __init__(self,account=None,deploy_txn=None,web3_port=8545,ipfs_port=5001):

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

        f = open('../contracts/ModelMine.sol','r')
        source = f.read()
        f.close()

        compiled = compile_source(source)['<stdin>:ModelMine']

        contract = self.web3.eth.contract(
            abi = compiled['abi'],
            bytecode = compiled['bin'],
            bytecode_runtime = compiled['bin-runtime'],
            source = source,
            )

        if(self.deploy_txn is None):
            self.deploy_txn = contract.deploy()
        txn_receipt = self.web3.eth.getTransactionReceipt(self.deploy_txn)
        contract_address = txn_receipt['contractAddress']

        self.transact = contract.transact({
            "from":self.web3.eth.accounts[2],
            "to":contract_address,
            })

        self.call = contract.call({
            "from":self.web3.eth.accounts[2],
            "to":contract_address,
            })

        return self.deploy_txn


    def submit_model(self,model):
        ipfs_address = self.ipfs.add_pyobj(model)
        deploy_trans = self.transact.addModel([ipfs_address[0:32],ipfs_address[32:]])
        return self.call.getNumModels()-1

    def __getitem__(self,model_id):
        if(model_id < len(self)):
            mca = self.call.getModel(model_id)
            model_client = self.ipfs.get_pyobj(str(mca[0]+mca[1]).split("\x00")[0])
            return model_client

    def __len__(self):
        return self.call.getNumModels()
