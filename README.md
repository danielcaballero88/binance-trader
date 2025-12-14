# Binance Trader

## Setup

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

1. Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. Clone the repo and navigate to it
3. Run `uv sync` to install dependencies
4. Run `uv run <script>` to execute scripts

For more info, see the [uv documentation](https://docs.astral.sh/uv/).

## Command runner

This project uses `just` as a unified and simple command runner. A `Justfile` is included at the repository root.

Installation and usage:

- Install `just`: see https://github.com/casey/just#installation for platform-specific instructions.
- List available commands: `just --list`
- Run a command: `just <recipe>` (for example `just test`)

Using `just` provides a single place for common tasks and makes running project commands consistent across environments.

## Environment Setup

## Linting & formatting

This project uses `ruff` as the unified linter and formatter. The `ruff` configuration lives in `pyproject.toml`.

Current notes about the configuration:

- The only customization at the moment is that we've added the "I" option for sorting imports so `ruff` can replace `isort` alongside the roles of `black` and `flake8`.

Common commands:

- Check code: `ruff check .`
- Fix and format: `ruff check --fix .` or `ruff format .`

See `pyproject.toml` for the full `ruff` settings.

See the `Justfile` for the most used commands.

### Secrets Management

For local development, sensitive values (API keys, tokens, database passwords, etc.) should be stored in a `.env` file in the project root and added to `.gitignore` to prevent accidental commits:

```
# .gitignore
.env
.env.local
```

### Using direnv for Automatic Secret Loading

It is recommended to use [direnv](https://direnv.net/) to automatically load environment variables when entering the project directory. This approach:

- Automatically sources the `.env` file when you `cd` into the project
- Unloads variables when you leave the directory
- Keeps your shell clean and prevents variable pollution

**Setup:**

1. Install direnv: https://direnv.net/docs/installation.html
2. Create a `.envrc` file in the project root with: `dotenv`
3. Run `direnv allow` to trust the `.envrc` file
