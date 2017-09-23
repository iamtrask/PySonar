import ipfsapi


class IPFS:
    def __init__(self, host='127.0.0.1', port=5001):
        self.host = host
        self.port = int(port)

    def connect(self):
        return ipfsapi.connect(self.host, self.port)

    def store(self, obj):
        return self.connect().add_pyobj(obj)

    def retrieve(self, ipfs_hash):
        return self.connect().get_pyobj(ipfs_hash)
