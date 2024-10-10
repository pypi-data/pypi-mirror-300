

poetry shell
poetry install

poetry add pytest requests-mock --group test


python 
from jolieprinter.printer import prettyprint

add test files to tests/

poetry run python jolieprinter/printer.py

poetry run pytest -v



# Sync Scripts 

## Testing

Run the tests using the following command:

```bash
pytest -v tests/test.py 
```

##### Test with pytest

```
> pytest tests
```

##### Test with nox

```
> nox --sessions tests
```

#### nox
list all sessions
> nox --list

list all sessions by activating only lint
> nox --list --sessions lint

Run a specific session called lint
> nox --sessions lint

Run a specific session called formatter
> nox --sessions formatter


Run a specific session called formatter
> nox --sessions tests


Run all the sessions in current noxfile:
> nox

Run a specific session ang generate a report:
>  nox --sessions tests --report nox-report.json


    - nox -f api/noxfile.py --list
    - nox -f api/noxfile.py -s formatter
    - nox -f api/noxfile.py --list
    - nox -f api/noxfile.py -s lint
    -  nox -f api/noxfile.py -s tests --report nox-report.json



-----------------------------
### Publication

#### Poetry

[Read more](https://python-poetry.org/docs/repositories/#install-dependencies-from-a-private-repository)

```
poetry config -h
poetry config --list
```

# Pypi publication

- https://packaging.python.org/en/latest/specifications/pypirc/#pypirc
- https://packaging.python.org/en/latest/guides/using-testpypi/
- https://packaging.python.org/en/latest/tutorials/packaging-projects/#uploading-your-project-to-pypi


## testpipy

poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config pypi-token.testpypi pypi-yt7yu
poetry publish --build --repository testpypi



python3 -m pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ jolieprinter


## pipy
poetry config repositories.pypi https://upload.pypi.org/legacy/
poetry config pypi-token.pypi pypi-fxMhRgf
poetry publish --build --repository pypi


### Installation

To install a PyPI package from the package registry, execute the following command:

```bash
pip install --index-url https://platform/packages/{owner}/pypi/simple/ cnaas-sync
```

Add a username and password if required:

```bash
pip install --index-url https://{username}:{password}@platform/packages/{owner}/pypi/simple/ cnaas-sync
```

Add the following extra index URL to download dependencies from the Python default package repository:

```bash
--extra-index-url https://pypi.org/simple
```

cnaas-sync-cli --config-file /opt/ni/cnaas_sync_config.ini -t nav