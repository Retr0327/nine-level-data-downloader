import re
import json
import asyncio
import aiohttp
from .urldialector import URLDialector
from dataclasses import dataclass, asdict
from typing import Awaitable, Dict, Any, Tuple, Union, List


__all__ = ["NineLevelDataDownloader"]

# --------------------------------------------------------------------
# helper functions


async def download_data(url) -> Awaitable[Dict[str, Any]]:
    """The download_data method downloads json data from the `url`.

    Args:
        url (str): the url that the user wants to download

    Returns:
        a dict: {
            'title': 'Kapah haw kisu?',
            'titleCh': '你好嗎？',
            'sentence': [
                {
                    'chinese': '你好嗎，老師？',
                    'order': '1',
                    'word': [
                        {
                            'ab': 'Kapah',
                            'ch': '好'
                        },
                        ...
                    ]
                },
                ...
            ]
        }

    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            while True:
                try:
                    html = await response.json(encoding="utf-8", content_type=None)
                    return html
                    break
                except json.decoder.JSONDecodeError:
                    continue



# --------------------------------------------------------------------
# public interface


@dataclass
class NineLevelDataCleanerInfo:
    """
    The DataInfo objects keeps track of an item in inventory, including order, dialect and chinese translation.`
    """

    order: str
    dialect: str
    chinese_translation: str


@dataclass
class NineLevelDataCleaner:
    """
    The NineLevelDataCleaner objects first extracts the target data from json, and then cleans it.
    """

    data: Dict[str, Any]

    # def __post_init__(self) -> None:
    #     self.data = asyncio.run(download_data(self.url))

    def concatenate_ab_value(self, dialect: list) -> str:
        """The concatenate_ab_value method concatenates the ab values from the dialect.

        Args:
            dialect (list): the list that contains the ab values

        Returns:
            a str
        """
        list_of_dialect_values = [
            translation_dict["ab"] for translation_dict in dialect
        ]
        dialect_values = " ".join(list_of_dialect_values)
        return re.sub("\s(?=\,|\?|\.|\:|\;|\!)", "", dialect_values)

    def extract_data(self, sentence_list: list):
        """The extract_data method extracts the data from the list that contains dialect sentences and chinese translations.

        Args:
            sentence_list (list): the list containing dialect sentences and chinese translations.

        Returns:
            a dict: {
                'order': '1',
                'dialect': 'Kapah haw kisu, pasebana’ay?',
                'chinese_translation': '你好嗎，老師？'},
            }
        """
        order = sentence_list["order"]
        chinese_translation = sentence_list["chinese"]
        dialect = sentence_list["word"]

        data = NineLevelDataCleanerInfo(
            order=order,
            dialect=self.concatenate_ab_value(dialect),
            chinese_translation=chinese_translation,
        )

        return asdict(data)

    def clean_data(self) -> Tuple[str, map]:
        """The clean_data method cleans json.

        Returns:
            a tuple
        """
        title = f"""{self.data["title"]} {self.data["titleCh"]}"""
        sentence_list = self.data["sentence"]
        return title, map(self.extract_data, sentence_list)


@dataclass
class NineLevelDataInfo:
    """
    The NineLevelDataInfo objects keeps track of an item in inventory, including level_id, class_id, title and data.
    """

    level_id: str
    class_id: str
    title: str
    data: list


@dataclass
class NineLevelDataDownloader:
    """
    The NineLevelDataDownloader object downloads the data.
    """

    url_dialector: URLDialector

    def __post_init__(self) -> None:
        self.request_info = self.url_dialector.generate()

    async def download_content(self, request_info: dict) -> Awaitable[Dict[str, Any]]:
        """The download_content method will first get the information from the argument `request_info`, including
           the url, level_id, and class_id. Then, the method downloads the data from the url, and uses
           NineLevelDataCleaner object to clean it.

        Args:
            request_info (dict): the request info that carries the main information

        Returns:
            a dict: {
                'level_id': '1',
                'class_id': '2',
                'title': 'Mwadringadringay su? 你好嗎？',
                'data: [
                    {
                        'order': '1',
                        'dialect': 'Sinsi, mwadringadringay su?',
                        'chinese_translation': '老師，您好嗎？',
                    },
                    ...
                ]

            }
        """
        url = request_info["url"]
        content = asyncio.run(download_data(url))
        result = NineLevelDataCleaner(content).clean_data()

        data = NineLevelDataInfo(
            level_id=request_info["level_id"],
            class_id=request_info["class_id"],
            title=result[0],
            data=list(result[-1]),
        )

        return asdict(data)

    async def download(self) -> Awaitable[Union[Dict[str, Any], List[Dict[str, Any]]]]:
        """The download method downloads the data by mapping `self.request_info` into the method `download_content`.

        Returns:
            a dict if the `self.request_info` is a dict, a list if the `self.request_info` is a list
        """
        if isinstance(self.request_info, dict):
            return await self.download_content(self.request_info)
        else: 
            return await asyncio.gather(
                *[self.download_content(info) for info in self.request_info]
            )
