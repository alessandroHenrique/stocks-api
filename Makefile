start:
	@docker-compose up

test:
	@docker-compose run --rm web pytest --cov --cov-report term-missing --disable-warnings
