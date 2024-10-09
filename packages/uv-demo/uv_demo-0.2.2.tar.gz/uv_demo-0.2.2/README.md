# `uv-demo` PyPI package

A demo for the `uv` package manager. Very useless.

## Setup and Execution

```bash
uv run uv-demo
```

This will install all dependencies (`uv sync`) and run the entrypoint script.

## Integration with GitHub Actions

### Running actions locally

You can use `act` to run GitHub Actions locally and speedup feedback. It can be installed as a GitHub CLI extension:

```bash
gh extension install https://github.com/nektos/gh-act^C
cp config/secrets.env.example config/secrets.env
# edit config/secrets.env with the required secrets
gh act --secret-file config/secrets.env
# select medium-sized image in first run.
```

+ [`act` installation](https://nektosact.com/installation/index.html)
+ [`act` usage](https://nektosact.com/usage/index.html)
