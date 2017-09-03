import json
import copy
import ipfsapi
from web3 import Web3, KeepAliveRPCProvider


class Gradient():
    def __init__(self, owner, grad_values, gradient_id, new_model_error=None,
                 new_weights=None):
        self.owner = owner
        self.grad_values = grad_values
        self.id = gradient_id

        self.new_model_error = new_model_error
        self.new_weights = new_weights


class Model():
    def __init__(self, owner, syft_obj, bounty, initial_error, target_error,
                 model_id=None, repo=None):
        self.owner = owner
        self.syft_obj = syft_obj
        self.bounty = bounty
        self.initial_error = initial_error
        self.best_error = None  # TODO: get this
        self.target_error = target_error
        self.model_id = model_id
        self.repo = repo

    def __getitem__(self, gradient_id):
        (gradient_id, grad_owner, mca, new_model_error,
         nwa) = self.repo.call.getGradient(self.model_id, gradient_id)
        grad_values = \
            self.repo.ipfs.get_pyobj(str(mca[0] + mca[1]).split("\x00")[0])
        if(new_model_error != 0):
            new_weights = \
                self.repo.ipfs.get_pyobj(str(nwa[0] + nwa[1]).split("\x00")[0])
        else:
            new_weights = None
            new_model_error = None
        g = Gradient(grad_owner, grad_values, gradient_id,
                     new_model_error, new_weights)
        return g

    def __len__(self):
        return self.repo.call.getNumGradientsforModel(self.model_id)

    def submit_gradient(self, owner, input, target):
        gradient = self.generate_gradient(owner, input, target)
        self.repo.submit_gradient(gradient.owner,
                                  self.model_id, gradient.grad_values)

    def generate_gradient(self, owner, input, target):
        grad_values = self.syft_obj.generate_gradient(input, target)
        gradient = Gradient(owner, grad_values, None)
        return gradient

    def evaluate_gradient(self, addr, gradient, prikey, pubkey, inputs,
                          targets, alpha=1):

        candidate = copy.deepcopy(self.syft_obj)
        candidate.weights -= gradient.grad_values * alpha
        candidate.decrypt(prikey)

        new_model_error = candidate.evaluate(inputs, targets)

        tx = self.repo.get_transaction(from_addr=addr)
        ipfs_address = self.repo.ipfs.add_pyobj(candidate.encrypt(pubkey))
        tx.evalGradient(gradient.id, new_model_error, [ipfs_address[0:32],
                        ipfs_address[32:]])

        return new_model_error

    def __str__(self):
        s = ""
        s += "Desc:" + str(self.syft_obj.desc) + "\n"
        s += "Owner:" + str(self.owner) + "\n"
        s += "Bounty:" + str(self.bounty) + "\n"
        s += "Initial Error:" + str(self.initial_error) + "\n"
        s += "Best Error:" + str(self.best_error) + "\n"
        s += "Target Error:" + str(self.target_error) + "\n"
        s += "Model ID:" + str(self.model_id) + "\n"
        s += "Num Grads:" + str(len(self)) + "\n"
        return s

    def __repr__(self):
        return self.__str__()


class ModelRepository():
    """This class is a python client wrapper around the ModelMine.sol contract,
    giving easy to use python functions around the contract's functionality. It
    currently assumes you're running on a local testrpc Ethereum blockchain."""

    def __init__(self, contract_address, account=None, deploy_txn=None,
                 ipfs_host='127.0.0.1', web3_host='localhost', web3_port=8545,
                 ipfs_port=5001):
        """Creates the base blockchain client object (web3), ipfs client object
        (ipfs), and deploys the compiled contract. Thus, it assumes that you're
        working with a local testrpc blockchain."""

        self.deploy_txn = deploy_txn
        self.web3 = Web3(KeepAliveRPCProvider(host=web3_host,
                                              port=str(web3_port)))
        self.ipfs = ipfsapi.connect(ipfs_host, int(ipfs_port))

        if(account is not None):
            self.account = account
        else:
            print("No account submitted... using default[2]")
            self.account = self.web3.eth.accounts[2]

        self.compile_and_deploy(contract_address)

        print("Connected to OpenMined ModelRepository:" +
              str(self.contract_address))

    def compile_and_deploy(self, contract_address, directory='contracts/'):
        """This contract selects the contract associated with this python
        interface compiles it, and deploys it to a locally hosted (testrpc)
        blockchain."""

        f = open('../abis/ModelRepository.abi', 'r')
        abi = json.loads(f.read())
        f.close()

        self.contract = self.web3.eth.contract(abi=abi)

        self.contract_address = contract_address

        self.call = self.contract.call({
            "from": self.web3.eth.accounts[2],
            "to": self.contract_address,
        })

        return self.deploy_txn

    def get_transaction(self, from_addr, value=None):
        """I consistently forget the conventions for executing transactions against
        compiled contracts. This function helps that to be easier for me."""

        txn = {}
        txn["from"] = from_addr
        txn["to"] = self.contract_address

        if value is not None:
            txn["value"] = int(value)

        transact_raw = self.contract.transact(txn)
        return transact_raw

    def submit_model(self, model):
        """This accepts a model from syft.nn, loads it into IPFS, and uploads
        the IPFS address to the blockchain.

        TODO: use best practices for storing IPFS addresses on the blockchain."""
        ipfs_address = self.ipfs.add_pyobj(model.syft_obj)
        deploy_tx = self.get_transaction(model.owner, value=self.web3.toWei(model.bounty, 'ether'))
        deploy_tx.addModel([ipfs_address[0:32], ipfs_address[32:]],
                           model.initial_error, model.target_error)
        return self.call.getNumModels() - 1

    def submit_gradient(self, from_addr, model_id, grad):
        """This accepts gradients for a model from syft.nn and uploads them to
        the blockchain (via IPFS), linked to a model by it's id.

        TODO: modify syft.nn to actually have a "getGradients()" method call so
        that there can be checks that keep people from uploading junk.
        Currently any python object could be uploaded (which is obviously
        dangerous)."""

        ipfs_address = self.ipfs.add_pyobj(grad)
        self.get_transaction(from_addr).addGradient(model_id,
                                                    [ipfs_address[0:32], ipfs_address[32:]])
        return self.call.getNumGradientsforModel(model_id) - 1

    def __getitem__(self, model_id):
        if(model_id < len(self)):

            (owner, bounty, initial_error, target_error, mca) = \
                self.call.getModel(model_id)
            syft_obj = \
                self.ipfs.get_pyobj(str(mca[0] + mca[1]).split("\x00")[0])
            model = Model(owner, syft_obj, self.web3.fromWei(bounty, 'ether'),
                          initial_error, target_error, model_id, self)

            return model

    def __len__(self):
        return self.call.getNumModels()
