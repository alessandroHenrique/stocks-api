start:
	@docker-compose up

test:
	@docker-compose run --rm -e DJANGO_SETTINGS_MODULE=config.settings.test web pytest --cov --cov-report term-missing --disable-warnings
