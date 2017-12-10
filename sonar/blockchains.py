from web3 import Web3, KeepAliveRPCProvider, HTTPProvider

def connect_ethereum_infura(access_token, chain='rinkeby'):
    return Web3(HTTPProvider('https://'+str(chain)+'.infura.io/'+str(access_token)))

def connect_ethereum_local(host, port):
    return Web3(KeepAliveRPCProvider(host=host, port=str(port)))    