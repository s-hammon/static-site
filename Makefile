test:
	@sh scripts/test.sh

run:
	@sh scripts/main.sh

dev-env:
	@sh scripts/setup-dev.sh

pretty:
	@ruff format && ruff check

.PHONY: test run dev-env pretty