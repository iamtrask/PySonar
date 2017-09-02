.PHONY: test import-abi

test:
	pytest

import-abi:
	npm install && \
	cp node_modules/@openmined/sonar/build/*.abi abis/