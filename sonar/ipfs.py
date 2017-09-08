import ipfsapi


class IPFS:
    def __init__(self, host='127.0.0.1', port=5001):
        self.ipfs = ipfsapi.connect(host, int(port))

    def store(self, obj):
        return self.ipfs.add_pyobj(obj)

    def retrieve(self, hash):
        return self.ipfs.get_pyobj(hash)
