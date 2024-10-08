# ruff: noqa: INP001, T201, UP006, UP035
# %%


from dbnomics_fetcher_toolbox.errors.base import FetcherToolboxError


class XXX(FetcherToolboxError):
    def __init__(self) -> None:
        msg = "foooooo"
        super().__init__(msg=msg)


str(XXX())
