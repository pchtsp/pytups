init:
	pip install pipenv --upgrade
	pipenv install --dev

test:
	pipenv run python -m unittest discover -s tests

