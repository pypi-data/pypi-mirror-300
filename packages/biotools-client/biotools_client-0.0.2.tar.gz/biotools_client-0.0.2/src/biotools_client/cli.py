"""Command line interface for :mod:`biotools_client`.

Why does this file exist, and why not put this in ``__main__``?
You might be tempted to import things from ``__main__``
later, but that will cause problems--the code will get executed twice:

- When you run ``python3 -m biotools_client`` python will
  execute``__main__.py`` as a script. That means there won't be any
  ``biotools_client.__main__`` in ``sys.modules``.
- When you import __main__ it will get executed again (as a module) because
  there's no ``biotools_client.__main__`` in ``sys.modules``.

.. seealso:: https://click.palletsprojects.com/en/8.1.x/setuptools/#setuptools-integration
"""

import click

__all__ = [
    "main",
]


@click.command()
@click.option("--force", is_flag=True, help="Overwrite existing files")
def main(force: bool) -> None:
    """CLI for biotools_client."""
    # import inside the CLI to make running the --help command faster
    from .api import get_raw_biotools_records

    get_raw_biotools_records(force=force)


if __name__ == "__main__":
    main()
