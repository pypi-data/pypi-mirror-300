from typing import Self
from urllib.parse import quote_plus

from dbnomics_data_model.json_utils import JsonObject

from dbnomics_fetcher_toolbox.partition_downloader.partitions.types import Partition

__all__ = ["UrlPartition"]


class UrlPartition(Partition):
    def __init__(self, url: str) -> None:
        super().__init__(partition_id=url)
        self.url = url

    @classmethod
    def from_json(cls, data: JsonObject) -> Self:
        url = data.get("url")
        if not isinstance(url, str):
            raise TypeError(url)

        return cls(url)

    @property
    def file_discriminator(self) -> str:
        return quote_plus(self.url)

    def to_json(self) -> JsonObject:
        return {"url": self.url}
