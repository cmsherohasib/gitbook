# DeepshieldLibrary(based on Python 3.12.3 version)

### Introduction
This software library (based on Python) connects account(verifier,creator), content creator(like device, app), content verier(like ai,deepfake) to the blockchain network in order to initialize, read and write blockchain transactions.
More detailed information in the Specification provided by Deepshield.


### GitLab commands
git remote set-url origin https://<username>:<password>@gitlab.com/secublox-platform/deepshieldlibrary.git
git remote -v
git status
git add .
git commit -m "Update ..."
git push origin main


### install library
# run commands from the same directory where pyproject.toml is located
python3 -m pip install --upgrade twine

# build libraray (set version in pyproject.toml and delete "dist/" directory)
python3 -m pip install --upgrade build
python3 -m build
# deploy package
python3 -m twine upload --repository testpypi dist/*
# install package
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps package-deepshield-lib
# install local build
pip3 install package-deepshield-lib


### initial
pip install wheel
pip install setuptools
pip install twine

### for testing
pip install pytest
pip install pytest-runner

# build library

python3 setup.py bdist_wheel

pip3 install dist/package_deepshield_lib-0.0.1-py3-none-any.whl
### install deepshield lib, change to setup.py directory, execute

pip install -e
### unistall
pip uninstall package-deepshield-lib

### Blockchian connection
smart-contarct will be updated in pararalel and to use this library it needs the newest version together with the ABI-file.
Current smart-contract of the Mission-Control-Contract:
<https://sepolia.arbiscan.io/address/0xfc3E0D6d2b7EBF6B01E7C19c8eF76EBF2f8b66D8#code>
assigned ABI to this smart-contract: MissionControlToken20231017.abi

Source-Code of the Smart-Contracts is stored in GitLab:
<https://gitlab.com/secublox-platform/deepshield-blockchain>


### tutorial: How to create a Python library
<https://medium.com/analytics-vidhya/how-to-create-a-python-library-7d5aea80cc3f>


### package
python3 setup.py sdist bdist_wheel
pip install twine

### upload
python3 -m twine upload --repository testpypi dist/*

pip install -i https://test.pypi.org/simple/ package-deepshield-lib

python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps package-deepshield-lib

from package_deepshield_lib import connection
connection.initialize_connection('<https://arbitrum-sepolia.core.chainstack.com/02233ea7ad5afbf2a952a04e8f5c693f>', '0xfc3E0D6d2b7EBF6B01E7C19c8eF76EBF2f8b66D8', 'deepshield.abi')

https://test.pypi.org/project/package-deepshield-lib/

python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps 

from package_deepshield_lib import connection

## Smart Contract information
Proxy Contract Address: 0xfc3E0D6d2b7EBF6B01E7C19c8eF76EBF2f8b66D8 (deepshield-Proxy.abi)
Without Proxy Contract Address: 0x8e1eb346094b06cb752392890e76b5d887a1ca55 (deepshield.abi)
