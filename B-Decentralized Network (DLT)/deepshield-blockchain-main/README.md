### Introduction

This smart-contracts manages image processing flow between Creator, Blockchain-Network, Devices (FPGA) and Verifier.
Current Deplyment: <https://testnet-zkevm.polygonscan.com/address/0xefb955525612c0568098a2663713ed761c0919fb#code>
Gitlab of the Blockchain libary to access this smart-contract by python:
<https://gitlab.com/secublox-platform/missioncontroldevicelibrary>

### OpenZeppelin
npm install @openzeppelin/contracts --force
npm install @openzeppelin/contracts/upgradeable --force
forge install OpenZeppelin/openzeppelin-contracts
forge install OpenZeppelin/openzeppelin-contracts-upgradeable

### GitLab commands

git remote set-url origin <https://<USER>:<PASSWORD>@gitlab.com:443/secublox-platform/blockchain.git>
git remote -v
git status
git add .
git commit -m "Initial commit"
git commit -m "Update ..."
git push origin main

### Polygon zkEVM Testnet, test ETH

<https://faucet.polygon.technology/>

## Foundry

**Foundry is a blazing fast, portable and modular toolkit for Ethereum application development written in Rust.**

Foundry consists of:

- **Forge**: Ethereum testing framework (like Truffle, Hardhat and DappTools).
- **Cast**: Swiss army knife for interacting with EVM smart contracts, sending transactions and getting chain data.
- **Anvil**: Local Ethereum node, akin to Ganache, Hardhat Network.
- **Chisel**: Fast, utilitarian, and verbose solidity REPL.

## Documentation

<https://book.getfoundry.sh/>

## Tutorial

<https://www.youtube.com/watch?v=fNMfMxGxeag>

## Usage

### Build

```shell
forge build
```

### Test

```shell
forge test
```

### Format

```shell
forge fmt
```

### Gas Snapshots

```shell
forge snapshot
```

### Anvil

```shell
anvil
```

### Deploy

```shell
### simulation
forge script script/Deepshield.s.sol:DeepshieldScript --rpc-url https://nd-078-703-280.p2pify.com/e54d7e2a99da6dd0ac18d20bd05cda1f --private-key 

### build, deloy and verify Lakoma / Secublox
forge create --rpc-url https://nd-078-703-280.p2pify.com/e54d7e2a99da6dd0ac18d20bd05cda1f --private-key 0x114f88fedc575bc334e35ef9a42cbbe6cca40070a57cb382bbd5f42ece04a9d1 --etherscan-api-key 86WINMZCT3KWQ5JTD6DASIR5CIZBFND7RW --verify src/Deepshield.sol:Deepshield --constructor-args 0x6C5080BEbd7230ABe66E17e403E225c2ED244907 0x6C5080BEbd7230ABe66E17e403E225c2ED244907 0x6C5080BEbd7230ABe66E17e403E225c2ED244907

### build, deloy and verify customer IABG
forge create --rpc-url https://nd-078-703-280.p2pify.com/e54d7e2a99da6dd0ac18d20bd05cda1f --private-key  --etherscan-api-key 86WINMZCT3KWQ5JTD6DASIR5CIZBFND7RW --verify src/Deepshield.sol:Deepshield --constructor-args 0x085E5E3578c1cCdac86CD1D0E6B8043FABB7b6b7 0x085E5E3578c1cCdac86CD1D0E6B8043FABB7b6b7 0x085E5E3578c1cCdac86CD1D0E6B8043FABB7b6b7


### download smart-contract abi by polygonscan

```

### blockchain-lib

pip uninstall blockchain-lib

### goto library

pip install -e .

### Cast

```shell
cast <subcommand>
```

### Help

```shell
forge --help
anvil --help
cast --help
```


### Deployement process

Preparation:

- Set ETHERSCAN_API_KEY in .env
- Set PRIVATE_KEY in .env
- Set RPC_URL in .env

```shell

### Compile
$ forge build

### Load env
$ source .env

### Load Admin, pauser and minter address
File: script/Deepshield.s.sol and Line No: 32

### deploy and verify
$ forge script script/Counter.s.sol:CounterScript --rpc-url <your_rpc_url> --private-key <your_private_key>
$ forge script script/Counter.s.sol:CounterScript --rpc-url https://arbitrum-sepolia.core.chainstack.com/32258c8f3b926ca5fdfe3ab42ed974de --private-key 


### example
$ forge script script/Deepshield.s.sol --rpc-url $RPC_URL --broadcast --private-key $PRIVATE_KEY  --verify $ETHERSCAN_API_KEY -vvvv

```

In Deployement process, Three contracts should be deployed,

    1. Proxy Admin contract, The contract links Proxy and Implementation.

    2. Implementaion contract, The smart contract provides functionality and logic.

    3. Proxy contract, The smart contract which user interacts with.
    
