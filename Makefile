.PHONY: unittest loadtest run
check_dirs := src tests

unittest:
	python -m pytest

loadtest:
	locust --config=load-test/locust.conf

run:
	uvicorn src.main:app --host 0.0.0.0 --reload --port 8080 --no-access-log --log-level=critical

check:
	black --check $(check_dirs)
	isort --check-only .
	flake8 $(check_dirs)

fix:
	black $(check_dirs)
	isort .
