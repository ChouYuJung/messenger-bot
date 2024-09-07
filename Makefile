install:
	poetry install --no-root

install-all:
	poetry install --no-root --with dev -E all

upgrade-deps:
	poetry update
	poetry export -f requirements.txt --output requirements.txt --without-hashes
	poetry export -f requirements.txt --with dev -E all --output requirements-all.txt --without-hashes

format-code:
	isort . && black .

create-secret-key:
	openssl rand -hex 32

test-make:
	echo "make test"