from sonar.ipfs import IPFS


def test_retrieval_of_stored_obj():
    storage = IPFS(host='127.0.0.1', port=5001)
    obj_to_store = {'foo': 'bar'}
    address = storage.store(obj_to_store)
    retrieved_obj = storage.retrieve(address)
    assert retrieved_obj == obj_to_store
