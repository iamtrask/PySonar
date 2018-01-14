.PHONY: test import-abi

test:
	pytest --flake8

import-abi:
	npm install && \
	cp node_modules/@openmined/sonar/build/contracts/*.abi abis/
