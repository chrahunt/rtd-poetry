# rtd-poetry

Shim to execute full installation of Poetry (including dev dependencies) during builds on Read The Docs.

`pyproject.toml` before:

```toml
[build-system]
requires = ["poetry>=0.12"]
build-backend = "poetry.masonry.api"
```

`pyproject.toml` after:

```toml
[build-system]
requires = ["poetry>=0.12", "rtd-poetry"]
build-backend = "rtd_poetry"
```
