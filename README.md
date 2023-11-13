### USAGE

```shell
cd /path/to/project
poetry env use /path/to/python/3.11.x/bin/python
poetry install
poetry run python app/main.py
```

### Profiling:

To profile:

1. Open main.py and wrap main function with `@profile` decorator
2. Run

```shell
poetry run python -m memory_profiler app/main.py
```