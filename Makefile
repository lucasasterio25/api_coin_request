install:
	pip install -r requirements.txt

db:
	docker compose up -d

test:
	pytest

run:
	python main.py health

init-db:
	python main.py init-db