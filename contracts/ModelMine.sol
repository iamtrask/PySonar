pragma solidity ^0.4.8;

contract ModelMine {

  Model[] models;
  Gradient[] grads;

  struct IPFS {
    bytes32 first;
    bytes32 second;
  }

  struct Gradient {
    address from;
    IPFS grads;
    uint model_id;
  }

  struct Model {

    address owner;

    IPFS weights;
    IPFS grads;

    uint bounty;

    uint initial_error;
    uint target_error;

  }

  function addModel(bytes32[] _weights, uint initial_error, uint target_error) payable returns(uint256 model_index) {

    IPFS memory weights;
    weights.first = _weights[0];
    weights.second = _weights[1];

    Model memory newModel;
    newModel.weights = weights;

    newModel.bounty = msg.value;
    newModel.owner = msg.sender;

    newModel.initial_error = initial_error;
    newModel.target_error = target_error;

    models.push(newModel);

    return models.length-1;
  }

  function addGradient(uint model_id, bytes32[] _grad_addr) returns(uint256 grad_index) {

    IPFS memory grad_addr;
    grad_addr.first = _grad_addr[0];
    grad_addr.second = _grad_addr[1];

    Gradient memory newGrad;
    newGrad.grads = grad_addr;
    newGrad.from = msg.sender;
    newGrad.model_id = model_id;

    grads.push(newGrad);

    return grads.length-1;
  }

  function getNumModels() constant returns(uint256 model_cnt) {
    return models.length;
  }

  function getNumGradientsforModel(uint model_id) constant returns (uint num) {
    num = 0;
    for (uint i=0; i<grads.length; i++) {
      if(grads[i].model_id == model_id) {
        num += 1;
      }
    }
    return num;
  }

  function getModel(uint model_i) constant returns (bytes32[]) {

    Model memory currentModel;
    currentModel = models[model_i];
    bytes32[] memory _weights = new bytes32[](2);

    _weights[0] = currentModel.weights.first;
    _weights[1] = currentModel.weights.second;

    return (_weights);
  }

}
