# List available commands
default:
    @just --list

# Run all tests
test:
    uv run pytest

# Run all tests and provide test coverage
test-coverage:
    uv run pytest --cov=binance_trader

# Run linting
lint:
    uv run ruff check .

# Run a script from your bin folder
scripts script_name:
    uv run bin/{{script_name}}
