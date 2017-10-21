from sonar.contracts import IPFSAddress


def test_transform_ethereum_representation_of_ipfshash_back_to_ipfshash():
    sample_ethereum_representation = \
        ["0x516d576d796f4d6f63746662416169457332473436677065556d687146524457",
         "0x364b576f3634793572353831567a303030303030303030303030303030303030"]
    assert IPFSAddress().from_ethereum(sample_ethereum_representation) \
        == "QmWmyoMoctfbAaiEs2G46gpeUmhqFRDW6KWo64y5r581Vz"
