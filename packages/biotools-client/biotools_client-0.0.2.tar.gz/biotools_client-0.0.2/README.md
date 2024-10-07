<!--
<p align="center">
  <img src="https://github.com/cthoyt/biotools-client/raw/main/docs/source/logo.png" height="150">
</p>
-->

<h1 align="center">
  bio.tools Client
</h1>

<p align="center">
    <a href="https://github.com/cthoyt/biotools-client/actions/workflows/tests.yml">
        <img alt="Tests" src="https://github.com/cthoyt/biotools-client/actions/workflows/tests.yml/badge.svg" /></a>
    <a href="https://pypi.org/project/biotools_client">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/biotools_client" /></a>
    <a href="https://pypi.org/project/biotools_client">
        <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/biotools_client" /></a>
    <a href="https://github.com/cthoyt/biotools-client/blob/main/LICENSE">
        <img alt="PyPI - License" src="https://img.shields.io/pypi/l/biotools_client" /></a>
    <a href='https://biotools_client.readthedocs.io/en/latest/?badge=latest'>
        <img src='https://readthedocs.org/projects/biotools_client/badge/?version=latest' alt='Documentation Status' /></a>
    <a href="https://codecov.io/gh/cthoyt/biotools-client/branch/main">
        <img src="https://codecov.io/gh/cthoyt/biotools-client/branch/main/graph/badge.svg" alt="Codecov status" /></a>  
    <a href="https://github.com/cthoyt/cookiecutter-python-package">
        <img alt="Cookiecutter template from @cthoyt" src="https://img.shields.io/badge/Cookiecutter-snekpack-blue" /></a>
    <a href='https://github.com/psf/black'>
        <img src='https://img.shields.io/badge/code%20style-black-000000.svg' alt='Code style: black' /></a>
    <a href="https://github.com/cthoyt/biotools-client/blob/main/.github/CODE_OF_CONDUCT.md">
        <img src="https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg" alt="Contributor Covenant"/></a>
</p>

An API client to [bio.tools](https://bio.tools).

`bio.tools` doesn't provide a first-party data download 
([see this issue](https://github.com/bio-tools/biotoolsRegistry/issues/601)), 
so this package implements an API wrapper to get the data in bulk.

## 💪 Getting Started

```python
from biotools_client import get_raw_biotools_records

raw_records = get_raw_biotools_records()
```

Note, this takes about 2 hours when it's run since each page only includes 10 records
and there's on the scale of 30K records (i.e., 3,000 requests need to be made).

The data is also uploaded to Zenodo under the CC BY 4.0 license at
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.13869529.svg)](https://doi.org/10.5281/zenodo.13869529).

Later, this package will implement a way to normalize the data from these
records to be more comfortable to work with (e.g., removing missing records, 
annotating ORCID identifiers for authors, making better key names).

## 🚀 Installation

The most recent release can be installed from
[PyPI](https://pypi.org/project/biotools_client/) with:

```shell
pip install biotools_client
```

The most recent code and data can be installed directly from GitHub with:

```shell
pip install git+https://github.com/cthoyt/biotools-client.git
```

## 👐 Contributing

Contributions, whether filing an issue, making a pull request, or forking, are appreciated. See
[CONTRIBUTING.md](https://github.com/cthoyt/biotools-client/blob/master/.github/CONTRIBUTING.md)
for more information on getting involved.

## 👋 Attribution

### ⚖️ License

The code in this package is licensed under the MIT License.

### 🍪 Cookiecutter

This package was created with [@audreyfeldroy](https://github.com/audreyfeldroy)'s
[cookiecutter](https://github.com/cookiecutter/cookiecutter) package using [@cthoyt](https://github.com/cthoyt)'s
[cookiecutter-snekpack](https://github.com/cthoyt/cookiecutter-snekpack) template.

## 🛠️ For Developers

<details>
  <summary>See developer instructions</summary>

The final section of the README is for if you want to get involved by making a code contribution.

### Development Installation

To install in development mode, use the following:

```bash
git clone git+https://github.com/cthoyt/biotools-client.git
cd biotools-client
pip install -e .
```

### Updating Package Boilerplate

This project uses `cruft` to keep boilerplate (i.e., configuration, contribution guidelines, documentation
configuration)
up-to-date with the upstream cookiecutter package. Update with the following:

```shell
pip install cruft
cruft update
```

More info on Cruft's update command is
available [here](https://github.com/cruft/cruft?tab=readme-ov-file#updating-a-project).

### 🥼 Testing

After cloning the repository and installing `tox` with `pip install tox tox-uv`, 
the unit tests in the `tests/` folder can be run reproducibly with:

```shell
tox -e py
```

Additionally, these tests are automatically re-run with each commit in a
[GitHub Action](https://github.com/cthoyt/biotools-client/actions?query=workflow%3ATests).

### 📖 Building the Documentation

The documentation can be built locally using the following:

```shell
git clone git+https://github.com/cthoyt/biotools-client.git
cd biotools-client
tox -e docs
open docs/build/html/index.html
``` 

The documentation automatically installs the package as well as the `docs`
extra specified in the [`pyproject.toml`](pyproject.toml). `sphinx` plugins
like `texext` can be added there. Additionally, they need to be added to the
`extensions` list in [`docs/source/conf.py`](docs/source/conf.py).

The documentation can be deployed to [ReadTheDocs](https://readthedocs.io) using
[this guide](https://docs.readthedocs.io/en/stable/intro/import-guide.html).
The [`.readthedocs.yml`](.readthedocs.yml) YAML file contains all the configuration you'll need.
You can also set up continuous integration on GitHub to check not only that
Sphinx can build the documentation in an isolated environment (i.e., with ``tox -e docs-test``)
but also that [ReadTheDocs can build it too](https://docs.readthedocs.io/en/stable/pull-requests.html).

#### Configuring ReadTheDocs

1. Log in to ReadTheDocs with your GitHub account to install the integration
   at https://readthedocs.org/accounts/login/?next=/dashboard/
2. Import your project by navigating to https://readthedocs.org/dashboard/import then clicking the plus icon next to
   your repository
3. You can rename the repository on the next screen using a more stylized name (i.e., with spaces and capital letters)
4. Click next, and you're good to go!

### 📦 Making a Release

#### Configuring Zenodo

[Zenodo](https://zenodo.org) is a long-term archival system that assigns a DOI to each release of your package.

1. Log in to Zenodo via GitHub with this link: https://zenodo.org/oauth/login/github/?next=%2F. This brings you to a
   page that lists all of your organizations and asks you to approve installing the Zenodo app on GitHub. Click "grant"
   next to any organizations you want to enable the integration for, then click the big green "approve" button. This
   step only needs to be done once.
2. Navigate to https://zenodo.org/account/settings/github/, which lists all of your GitHub repositories (both in your
   username and any organizations you enabled). Click the on/off toggle for any relevant repositories. When you make
   a new repository, you'll have to come back to this

After these steps, you're ready to go! After you make "release" on GitHub (steps for this are below), you can navigate
to https://zenodo.org/account/settings/github/repository/cthoyt/biotools-client
to see the DOI for the release and link to the Zenodo record for it.

#### Registering with the Python Package Index (PyPI)

You only have to do the following steps once.

1. Register for an account on the [Python Package Index (PyPI)](https://pypi.org/account/register)
2. Navigate to https://pypi.org/manage/account and make sure you have verified your email address. A verification email
   might not have been sent by default, so you might have to click the "options" dropdown next to your address to get to
   the "re-send verification email" button
3. 2-Factor authentication is required for PyPI since the end of 2023 (see
   this [blog post from PyPI](https://blog.pypi.org/posts/2023-05-25-securing-pypi-with-2fa/)). This means
   you have to first issue account recovery codes, then set up 2-factor authentication
4. Issue an API token from https://pypi.org/manage/account/token

#### Configuring your machine's connection to PyPI

You have to do the following steps once per machine. Create a file in your home directory called
`.pypirc` and include the following:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = <the API token you just got>

# This block is optional in case you want to be able to make test releases to the Test PyPI server
[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = <an API token from test PyPI>
```

Note that since PyPI is requiring token-based authentication, we use `__token__` as the user, verbatim.
If you already have a `.pypirc` file with a `[distutils]` section, just make sure that there is an `index-servers`
key and that `pypi` is in its associated list. More information on configuring the `.pypirc` file can
be found [here](https://packaging.python.org/en/latest/specifications/pypirc).

#### Uploading to PyPI

After installing the package in development mode and installing
`tox` with `pip install tox tox-uv`,
run the following from the shell:

```shell
tox -e finish
```

This script does the following:

1. Uses [Bump2Version](https://github.com/c4urself/bump2version) to switch the version number in
   the `pyproject.toml`, `CITATION.cff`, `src/biotools_client/version.py`,
   and [`docs/source/conf.py`](docs/source/conf.py) to not have the `-dev` suffix
2. Packages the code in both a tar archive and a wheel using [`build`](https://github.com/pypa/build)
3. Uploads to PyPI using [`twine`](https://github.com/pypa/twine).
4. Push to GitHub. You'll need to make a release going with the commit where the version was bumped.
5. Bump the version to the next patch. If you made big changes and want to bump the version by minor, you can
   use `tox -e bumpversion -- minor` after.

#### Releasing on GitHub

1. Navigate
   to https://github.com/cthoyt/biotools-client/releases/new
   to draft a new release
2. Click the "Choose a Tag" dropdown and select the tag corresponding to the release you just made
3. Click the "Generate Release Notes" button to get a quick outline of recent changes. Modify the title and description
   as you see fit
4. Click the big green "Publish Release" button

This will trigger Zenodo to assign a DOI to your release as well.

</details>
