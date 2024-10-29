###############################################################################
#
#EoxCore commands.
#
###############################################################################

# Define PIP_COMPILE_OPTS=-v to get more information during make upgrade.
PIP_COMPILE = pip-compile --rebuild --upgrade $(PIP_COMPILE_OPTS)

.DEFAULT_GOAL := help

ifdef TOXENV
TOX := tox -- #to isolate each tox environment if TOXENV is defined
endif

# Generates a help message. Borrowed from https://github.com/pydanny/cookiecutter-djangopackage.
help: ## Display this help message
	@echo "Please use \`make <target>' where <target> is one of"
	@perl -nle'print $& if m{^[\.a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

bumpversion: ## Tag the current version using semantinc versioning and git tags (default: minor)
	# bumpversion major
	bumpversion minor
	# bumpversion patch

install-dev-dependencies: ## install tox
	pip install -r requirements/tox.txt
	pip install -r requirements/test.txt

clean: ## Remove generated byte code, coverage reports, and build artifacts
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	$(TOX) coverage erase
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

python-test: clean ## Run tests
	$(TOX) pip install -r requirements/test.txt --exists-action w
	$(TOX) coverage run --source="." -m pytest ./eox_core --ignore-glob='**/integration/*'
	$(TOX) coverage report --fail-under=70

python-quality-test:
	$(TOX) pycodestyle ./eox_core
	$(TOX) pylint ./eox_core
	$(TOX) isort --check-only --diff ./eox_core

run-tests: python-test python-quality-test

run-integration-tests: install-dev-dependencies
	# pytest -rPf ./eox_core --ignore-glob='**/unit/*' --ignore-glob='**/edxapp_wrapper/*'
	pytest -rPf ./eox_core --ignore-glob='**/unit/*' --ignore-glob='**/edxapp_wrapper/*' --ignore-glob='**/api/*'

upgrade: export CUSTOM_COMPILE_COMMAND=make upgrade
upgrade: ## update the requirements/*.txt files with the latest packages satisfying requirements/*.in
	pip install -qr requirements/pip-tools.txt
	# Make sure to compile files after any other files they include!
	$(PIP_COMPILE) -o requirements/pip-tools.txt requirements/pip-tools.in
	$(PIP_COMPILE) -o requirements/base.txt requirements/base.in
	$(PIP_COMPILE) -o requirements/test.txt requirements/test.in
	$(PIP_COMPILE) -o requirements/tox.txt requirements/tox.in

	grep -e "^django==" requirements/test.txt > requirements/django42.txt
	sed '/^[dD]jango==/d;' requirements/test.txt > requirements/test.tmp
	mv requirements/test.tmp requirements/test.txt
