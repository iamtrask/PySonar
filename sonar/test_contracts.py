from sonar.contracts import IPFSAddress


def can_transform_ipfs_hash_to_its_ethereum_representation():
    sample_ipfs_hash = "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG"
    assert IPFSAddress().to_ethereum(sample_ipfs_hash) \
        == ["QmYwAPJzv5CZsnA625s3Xf2nemtYgPpH", "dWEz79ojWnPbdG"]


def can_transform_ethereum_representation_of_ipfshash_back_to_ipfshash():
    sample_ethereum_representation = \
        "0x516d576d796f4d6f63746662416169457332473436677065556d687146524457"
    assert IPFSAddress().from_ethereum(sample_ethereum_representation) \
        == "QmWmyoMoctfbAaiEs2G46gpeUmhqFRDW6KWo64y5r581Vz"
