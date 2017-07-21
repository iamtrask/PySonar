pragma solidity ^0.4.8;

contract ModelMine {

  Model[] models;

  struct IPFS {
    bytes32 first;
    bytes32 second;
  }

  struct Model {
    IPFS weights;
  }

  function addModel(bytes32[] _weights) returns(uint256 model_index) {

    IPFS memory weights;
    weights.first = _weights[0];
    weights.second = _weights[1];

    Model memory newModel;
    newModel.weights = weights;
    models.push(newModel);

    return models.length-1;
  }

  function getNumModels() returns(uint256 model_cnt) {
    return models.length;
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
